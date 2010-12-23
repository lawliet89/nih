from urllib import urlretrieve
from os.path import join, exists, abspath
from os import mkdir
from models import QueueItem
from metadata import get_metadata

cacheFolder = "cache"

def cached(item):
	hash = item.hash()
	cacheFile = join(cacheFolder, hash)
	if not exists(cacheFile):
		urlretrieve(item.url, cacheFile)
		assert exists(cacheFile)
	
	if not item.got_metadata:
		metadata = get_metadata(cacheFile)
		item.artist = metadata["artistName"]
		item.album = metadata["albumTitle"]
		item.title = metadata["trackName"]
		item.trackLength = metadata["totalTime"]
		item.trackNumber = metadata["trackNumber"]
		item.got_metadata = True
		item.save()

	return abspath(cacheFile)

if not exists(cacheFolder):
	mkdir(cacheFolder)
for x in QueueItem.objects.all():
	cached(x.what)
