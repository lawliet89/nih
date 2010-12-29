from django.test import TestCase
from django.test.client import Client
from jsonrpc._json import loads, dumps
from uuid import uuid1
from jukebox.models import *

class JukeboxTest(TestCase):
	def setUp(self):
		self.client = Client()

	def _method(self, method, *params):
		req = {
		  u'version': u'1.1',
		  u'method': method,
		  u'params': params,
		  u'id': u'random_test_id'
		}
		return self._call(req)
	
	def _call(self, req):
		return loads(self.client.post("/rpc/jukebox", dumps(req), content_type="application/json").content)[u'result']

	def _addTestTrack(self):
		url = "http://localhost/"+uuid1().hex
		m = MusicFile()
		m.url = url
		m.save()
		return url

	def _enqueueTestTrack(self):
		url = self._addTestTrack()
		resp = self._method("enqueue", "test_user", [{"url":url}], False)
		return (url, resp)

	def testEnqueue(self):
		(url, res) = self._enqueueTestTrack()
		self.assertEquals(res[u'entry'][u'url'], url)
		self.assertEquals(res[u'entry'][u'username'], "test_user")
		self.assertEquals(res[u'queue'], [])

	def testSkip(self): 
		QueueItem.objects.all().delete() # clear anything else in there

		(url, _) = self._enqueueTestTrack()
		(url2, _) = self._enqueueTestTrack()

		res = self._method("get_queue")
		self.assertEqual(res['entry']['url'], url, res)
		res = self._method("skip", "test_user")
		self.assertEqual(res['entry']['url'], url2, res)
		res = self._method("skip", "test_user")
		self.assertEqual(res['entry'], None, res)
