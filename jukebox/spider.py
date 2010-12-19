from threading import Thread
from models import WebPath, MusicFile
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen, HTTPError
from urlparse import urljoin
from os.path import splitext

_spider = None

def get_spider():
	global _spider
	if _spider == None:
		_spider = Spider()
		_spider.setDaemon(True)
	if not _spider.isAlive():
		try:
			_spider.start()
		except RuntimeError,e:
			 # already started, so need to recreate
			 _spider = None
			 return get_spider()
				 
	return _spider

known_extensions = [".mp3", ".ogg", ".flac", ".wma", ".mp4"]

class Spider(Thread):
	def todo(self):
		return WebPath.objects.filter(checked=False, failed=False)

	def run(self):
		while True:
			items = self.todo()
			if len(items) == 0:
				break
			current = items[0]
			print "path", current.url

			try:
				page = urlopen(current.url)
			except HTTPError:
				current.failed = True
				current.save()
				continue
			url = page.geturl()
			soup = BeautifulSoup(page)
			for link in soup.findAll("a"):
				resolved = urljoin(url, link["href"])
				if len(resolved) < len(url): # up link, skip
					print "skipping",resolved
					continue
				if resolved[-1] == "/": # directory
					if len(WebPath.objects.filter(url=resolved)) == 0:
						current.add_sibling(url=resolved)
						current = WebPath.objects.get(pk=current.id) # work around treebeard issues
				else: # file?
					(_, ext) = splitext(resolved)
					ext = ext.lower()
					if ext in known_extensions:
						if len(MusicFile.objects.filter(url=resolved)) == 0:
							mf = MusicFile(url = resolved)
							mf.save()
					else:
						print "Can't handle", resolved, ext, len(ext)

			current.checked = True
			current.save()
