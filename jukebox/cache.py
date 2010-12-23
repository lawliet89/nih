from urllib import urlretrieve
from os.path import join, exists, abspath
from os import mkdir
from models import QueueItem
from metadata import get_metadata
from threading import Thread, Lock, Condition
from Queue import Queue
from jsonfuncs import *

cacheFolder = "cache"

class Downloader(Thread):
	queue = []
	queueCondition = Condition()

	def run(self):
		while True:
			self.queueCondition.acquire()
			self.queueCondition.wait()
			if len(self.queue)>0: # should always be true here, but just in case
				item = self.queue[0] # don't remove it yet though
			else:
				item = None
			self.queueCondition.release()
			if item == None:
				continue

			hash = item.hash()
			cacheFile = join(cacheFolder, hash)
			urlretrieve(item.url, cacheFile)
			assert exists(cacheFile)
			cached(item)

			self.queueCondition.acquire()
			assert len(self.queue)>0
			assert self.queue[0] == item, (item, self.queue)
			self.queue = self.queue[1:]
			self.queueCondition.release()

			if QueueItem.current() == item and status == Status.playing:
				play_current()
	
	def downloads(self):
		self.queueCondition.acquire()
		ret = list(self.queue)
		self.queueCondition.release()
		return ret

	def new(self, item):
		self.queueCondition.acquire()
		self.queue.append(item)
		self.queueCondition.notify()
		self.queueCondition.release()

downloader = Downloader()
downloader.setDaemon(True)
downloader.start()

def is_cached(item):
	hash = item.hash()
	cacheFile = join(cacheFolder, hash)
	return exists(cacheFile)

def cached(item):
	hash = item.hash()
	cacheFile = join(cacheFolder, hash)
	if not is_cached(item):
		downloader.new(item)
		return None
	
	if not item.got_metadata:
		metadata = get_metadata(cacheFile)
		item.artist = metadata.get("artistName", "")
		item.album = metadata.get("albumTitle", "")
		item.title = metadata.get("trackName", "")
		item.trackLength = metadata.get("totalTime", 0)
		item.trackNumber = metadata.get("trackNumber", "0")
		item.got_metadata = True
		item.save()

	return abspath(cacheFile)

if not exists(cacheFolder):
	mkdir(cacheFolder)
for x in QueueItem.objects.all():
	cached(x.what)
