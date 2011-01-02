from os.path import join, dirname
import urllib2
from threading import Thread, Lock, Condition

client = None
HTTPError = urllib2.HTTPError

def site_path(path):
	return join(dirname(__file__), path)

class FakeURLObject:
	def __init__(self, backing, url):
		self.backing = backing
		self.url = url

	def geturl(self):
		return self.url

	def read(self):
		return self.backing.content

def urlopen(url):
	try:
		return urllib2.urlopen(url)
	except HTTPError:
		global client
		if client == None:
			from django.test.client import Client
			client = Client()
		local = "http://localhost"
		if url.find(local) != -1: # assume local server attempt, so try test client
			path = url[len(local):]
			obj = client.get(path)
			if obj.status_code != 200:
				raise
			return FakeURLObject(obj, url)
		else:
			raise

class BackgroundTask(Thread):
	def __init__(self):
		self.queue = []
		Thread.__init__(self)
		self.queueCondition = Condition()

	def todo(self):
		with self.queueCondition:
			return list(self.queue)

	def run(self):
		self.startup()
		while True:
			with self.queueCondition:
				while True:
					if len(self.queue)>0:
						item = self.queue[0] # don't remove it yet though (still needs to be marked as "caching")
						break
					else:
						print "waiting", self
						self.queueCondition.wait()

			self.processItem(item)

			with self.queueCondition:
				assert len(self.queue)>0
				assert self.queue[0] == item, (item, self.queue)
				self.queue = self.queue[1:]
			
			self.postProcessItem(item)	

	def add(self, item):
		with self.queueCondition:
			self.queue.append(item)
			print "got item for", self, item
			self.queueCondition.notify()

	def startup(self):
		pass
	
	def processItem(self):
		raise Exception, "Subclasses must implement processItem"

	def postProcessItem(self, item):
		pass

startup_tasks = []
started = False

def registerStartupTask(task):
	global startup_tasks, started
	startup_tasks.append(task)
	if started:
		task.start()

def runStartupTasks(sender, **kwargs):
	global startup_tasks, started
	if started:
		return
	started = True
	for t in startup_tasks:
		t.start()

