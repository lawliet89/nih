from utils import urlopen, HTTPError, BackgroundTask, registerStartupTask
from os.path import join, exists, abspath
from os import mkdir
from models import QueueItem, ChatItem
from metadata import get_metadata
from Queue import Queue
import jsonfuncs

cacheFolder = "cache"

class Downloader(BackgroundTask):
	def processItem(self,item):
		hash = item.hash()
		cacheFile = join(cacheFolder, hash)
		try:
			data = urlopen(item.url).read()
			open(cacheFile, "wb").write(data)
			cached(item)
		except HTTPError:
			item.failed = True
			item.save()

	def postProcessItem(self, item):
		if item.failed:
			print "item failed", item
			char = ChatItem(what="failed", info = item)
			char.save()
			if QueueItem.current()!=None:
				jsonfuncs.next_track()
		elif QueueItem.current() == item and status == Status.playing:
			jsonfuncs.play_current()
	
	def downloads(self):
		with self.queueCondition:
			ret = list(self.queue)
			return ret

downloader = registerStartupTask(Downloader)

def is_cached(item):
	hash = item.hash()
	cacheFile = join(cacheFolder, hash)
	return exists(cacheFile)

def cached(item):
	hash = item.hash()
	cacheFile = join(cacheFolder, hash)
	if not is_cached(item):
		downloader.add(item)
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
