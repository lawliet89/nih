from jsonrpc import jsonrpc_method
from models import *
from time import mktime
from urllib import unquote
from random import sample
from alsaaudio import Mixer

@jsonrpc_method('get_caller_hostname')
def hostname(request):
	if request.META["REMOTE_HOST"] != "":
		return request.META["REMOTE_HOST"]
	else:
		return request.META["REMOTE_ADDR"]

def status_info(request):
	return {
			"status":"idle",
			"entry":None,
			"info": {},
			"queue": [x.what.url for x in QueueItem.objects.all()],
			"queueInfo": [],
			"paused": True,
			"elapsedTime": 0,
			"downloads": []
		}

@jsonrpc_method('search')
def search(request, inp):
	items = MusicFile.objects
	for term in inp:
		items = items.filter(url__contains=term)
	return [{"url":x.url} for x in items]

@jsonrpc_method('randomtracks')
def randomtracks(request, count):
	items = MusicFile.objects.all()
	ret = [{"url":items[x].url} for x in sample(range(items.count()),count)]
	return ret

@jsonrpc_method('enqueue')
def enqueue(request, username, tracks, atTop):
	for t in tracks:
		q = QueueItem(who = username, what = MusicFile.objects.get(url=t['url']))
		try:
			if atTop:
				q.index = QueueItem.objects.all().order_by("index")[0].index - 1
			else:
				q.index = QueueItem.objects.order_by("-index")[0].index + 1
		except IndexError: # nothing else in queue
			q.index = 0
		q.save()
	return status_info(request)

@jsonrpc_method('dequeue')
def dequeue(request):
	return ""

@jsonrpc_method('get_queue')
def get_queue(request):
	return status_info(request)

volume_who = ""
volume_direction = ""

def volume():
	volume = Mixer().getvolume()
	return {"volume":volume[0], "who":volume_who, "direction": volume_direction}

@jsonrpc_method('get_volume')
def get_volume(request):
	return volume()

@jsonrpc_method('set_volume')
def set_volume(request, username, value):
	global volume_who, volume_direction
	m = Mixer()
	if value > m.getvolume()[0]:
		volume_direction = "up"
		volume_who = username
	elif value < m.getvolume()[0]:
		volume_direction = "down"
	else:
		return volume() # no change, quit
	
	volume_who = username
	m.setvolume(value)
	return volume()


def chat_history(request, limit):
	return [{"when":mktime(x.when.timetuple()),"who":x.who, "what":x.what, "message":x.message, "track":x.info} for x in ChatItem.objects.all()[:limit]]

@jsonrpc_method('chat')
def chat(request, username, text):
	item = ChatItem(what="says", message=text, who=username)
	item.save()

@jsonrpc_method('get_history')
def get_history(request, limit):
	return chat_history(request, limit)

