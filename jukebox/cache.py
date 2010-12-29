from urllib2 import urlopen, HTTPError
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
			with self.queueCondition:
				while True:
					if len(self.queue)>0:
						item = self.queue[0] # don't remove it yet though (still needs to be marked as "caching")
						break
					else:
						self.queueCondition.wait()

			hash = item.hash()
			cacheFile = join(cacheFolder, hash)
			try:
				data = urlopen(item.url).read()
				open(cacheFile, "wb").write(data)
				cached(item)
			except HTTPError:
				item.failed = True
				item.save()

			with self.queueCondition:
				assert len(self.queue)>0
				assert self.queue[0] == item, (item, self.queue)
				self.queue = self.queue[1:]

			if QueueItem.current() == item and status == Status.playing:
				if item.failed:
					char = ChatItem(what="failed", info = item.what)
					chat.save()
					next_track()
				else:
					play_current()
	
	def downloads(self):
		with self.queueCondition:
			ret = list(self.queue)
			return ret

	def new(self, item):
		with self.queueCondition:
			self.queue.append(item)
			self.queueCondition.notify()

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

def albumArt(item):
	cacheFile = join(cacheFolder, item.hash() + ".jpeg")
	if exists(cacheFile):
		return cacheFile
	else:
		return None

if not exists(cacheFolder):
	mkdir(cacheFolder)
for x in QueueItem.objects.all():
	cached(x.what)
