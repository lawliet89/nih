from urllib import urlretrieve
from os.path import join, exists, abspath
from os import mkdir
from models import QueueItem

cacheFolder = "cache"

def cached(item):
	hash = item.hash()
	cacheFile = join(cacheFolder, hash)
	if not exists(cacheFile):
		urlretrieve(item.url, cacheFile)
		assert exists(cacheFile)
	return abspath(cacheFile)

if not exists(cacheFolder):
	mkdir(cacheFolder)
for x in QueueItem.objects.all():
	cached(x.what)
