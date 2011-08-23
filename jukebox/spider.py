from models import WebPath, MusicFile
from BeautifulSoup import BeautifulSoup
from utils import urlopen, HTTPError, BackgroundTask, registerStartupTask
from urlparse import urljoin
from os.path import splitext

known_extensions = [".mp3", ".ogg", ".flac", ".wma", ".m4a"]

class Spider(BackgroundTask):
	def startup(self):
		for x in WebPath.objects.filter(checked=False, failed=False):
			self.add(x)

	def processItem(self, current):
		try:
			page = urlopen(current.url)
		except HTTPError:
			print "fail", current.url
			current.failed = True
			current.save()
			return
		url = page.geturl()
		soup = BeautifulSoup(page)
	
		for link in soup.findAll("a"):
			resolved = urljoin(url, link["href"])
			if len(resolved) < len(url): # up link, skip
				print "skipping",resolved, url
				continue
			if resolved[-1] == "/": # directory
				if WebPath.objects.filter(url=resolved).count() == 0:
					child = current.add_child(url=resolved)
					self.add(child)
			else: # file?
				(_, ext) = splitext(resolved)
				ext = ext.lower()
				if ext in known_extensions:
					if MusicFile.objects.filter(url=resolved).count() == 0:
						mf = MusicFile(parent=current, url = resolved)
						mf.save()
				else:
					print "Can't handle", resolved, ext, len(ext)

		current.checked = True
		current.save()

spider = registerStartupTask(Spider)
