from django.test import TestCase
from django.test.client import Client
from jsonrpc._json import loads, dumps
from uuid import uuid1
from jukebox.models import *
from time import sleep
import utils
from spider import spider
from jsonfuncs import downloader

class JukeboxTest(TestCase):
	static_path = "http://localhost/static/"

	def setUp(self):
		utils.client = self.client
		self._method("rescan_root", self.static_path)

	def needs_static(self):
		while len(spider.todo())>0:
			print "spider todo", spider.todo()
			sleep(.5)

	def needs_downloaded(self):
		while len(downloader.todo())>0:
			print "downloader todo", downloader.todo()
			sleep(.5)

	def clear_queue(self):
		QueueItem.objects.all().delete() # clear anything else in there

	def _method(self, method, *params):
		req = {
		  u'version': u'1.1',
		  u'method': method,
		  u'params': params,
		  u'id': u'random_test_id'
		}
		return self._call(req)
	
	def _call(self, req):
		resp = loads(self.client.post("/rpc/jukebox", dumps(req), content_type="application/json").content)
		self.assert_("result" in resp.keys(), resp)
		return resp["result"]

	def _addTestTrack(self, url = None):
		if url == None:
			url = "http://localhost/"+uuid1().hex
		if MusicFile.objects.filter(url = url).count() == 0:
			m = MusicFile()
			m.url = url
			m.save()
			print "added test track", url
		else:
			print "test track already present", url
		return url

	def _enqueueTestTrack(self):
		url = self._addTestTrack()
		resp = self._method("enqueue", "test_user", [{"url":url}], False)
		return (url, resp)

	def _enqueueRealTrack(self):
		self.needs_static()
		url = self._addTestTrack(self.static_path+"silent-3mins.mp3")
		resp = self._method("enqueue", "test_user", [{"url":url}], False)
		return (url, resp)

	def testEnqueue(self):
		(url, res) = self._enqueueTestTrack()
		self.assertEquals(res[u'entry'][u'url'], url)
		self.assertEquals(res[u'entry'][u'username'], "test_user")
		self.assertEquals(res[u'queue'], [])

	def testPlay(self): 
		self.clear_queue()
		res = self._method("pause", False)
		self.assertEqual(res['status'], "idle", res)
		self.assertEqual(res['entry'], None, res)
		self.assertEqual(res['queue'], [], res)

		(url, _) = self._enqueueTestTrack()
		res = self._method("pause", False)
		self.assertEqual(res['paused'], False, res)
		self.assertEqual(res['status'], "caching", res)

	def testSkip(self): 
		self.clear_queue()

		(url, _) = self._enqueueRealTrack()
		(url2, _) = self._enqueueRealTrack()

		res = self._method("get_queue")
		self.assertEqual(res['entry']['url'], url, res)
		res = self._method("skip", "test_user")
		self.assertEqual(res['entry']['url'], url2, res)
		res = self._method("skip", "test_user")
		self.assertEqual(res['entry'], None, res)

	def testSkipWithPlay(self): 
		(url, _) = self._enqueueRealTrack()
		(url2, _) = self._enqueueRealTrack()

		self.needs_downloaded()
		res = self._method("pause", False)
		self.assertNotEqual(res['entry'], None, res)
		self.assertEqual(res['entry']['url'], url, res)
		self.assertEqual(res['paused'], False, res)
		self.assertEqual(res['status'], "playing", res)

		res = self._method("skip", "test_user")
		self.assertEqual(res['entry']['url'], url2, res)

		res = self._method("skip", "test_user")
		self.assertEqual(res['entry'], None, res)

	def testPlay(self):
		self.clear_queue()

		res = self._method("pause", False)
		self.assertEqual(res['entry'], None, res)
		(url, _) = self._enqueueRealTrack()
		res = self._method("pause", False)
		self.needs_downloaded()
		self.assertEqual(res['paused'], False, res)
		self.assertEqual(res['status'], "playing", res)

	def testNotCachedYet(self):
		print "starting cache test"
		self.clear_queue()
		downloader.pause()

		(url, _) = self._enqueueTestTrack()
		(url2, _) = self._enqueueTestTrack()

		res = self._method("pause", False)
		self.assertNotEqual(res['entry'], None, res)
		self.assertEqual(res['entry']['url'], url, res)
		res = self._method("skip", "test_user")
		self.assertNotEqual(res['entry'], None, res)
		self.assertEqual(res['entry']['url'], url2, res)
		res = self._method("skip", "test_user")
		self.assertEqual(res['entry'], None, res)

		downloader.unpause()
