from jsonrpc import jsonrpc_method
from models import *
from time import mktime
from urllib import unquote
from random import sample
from alsaaudio import Mixer
import pygst
pygst.require("0.10")
import gst
from enum import Enum
from cache import *
from threading import Thread
import gobject

@jsonrpc_method('get_caller_hostname')
def hostname(request):
	if request.META["REMOTE_HOST"] != "":
		return request.META["REMOTE_HOST"]
	else:
		return request.META["REMOTE_ADDR"]

class Status(Enum):
	idle = 1
	playing = 2
	paused = 3

status = Status.idle

def metadata(item):
	return {"artistName":item.artist, "albumTitle":item.album, "trackName":item.title, "trackNumber":item.trackNumber}

def status_info(request):
	items = [{"id":x.id, "url":x.what.url, "username":x.who} for x in QueueItem.objects.all()]
	itemsMeta = [metadata(x.what) for x in QueueItem.objects.all()]
	if len(items)>0:
		first = (items[0], itemsMeta[0])
	else:
		first = (None, None)

	if status == Status.idle:
		elapsed = 0
		totalTime = 0
	else:
		try:
			elapsed, format = player.query_position(gst.Format(gst.FORMAT_TIME), None)
			elapsed /= gst.SECOND
			totalTime, format = player.query_duration(gst.Format(gst.FORMAT_TIME), None)
			totalTime /= gst.SECOND
		except gst.QueryError, e:
			print "e",e
			elapsed = 0
			totalTime = 0

	if QueueItem.current()!=None and QueueItem.current().what in downloader.downloads():
		state = "caching"
	else:
		state = status.name()

	return {
		"status":state,
		"entry":first[0],
		"info": first[1],
		"queue": items[1:],
		"queueInfo": itemsMeta[1:],
		"paused": status != Status.playing,
		"elapsedTime": elapsed,
		"downloads": [x.url for x in downloader.downloads()]
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
		cached(q.what)
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
def dequeue(request, username, track):
	queue = list(QueueItem.objects.all())[1:]
	for item in queue:
		if item.id == track["id"]:
			item.delete()
	return status_info(request)

@jsonrpc_method('clear_queue')
def clear_queue(request, username):
	queue = list(QueueItem.objects.all())[1:]
	for item in queue:
		item.delete()
	return status_info(request)

@jsonrpc_method('get_queue')
def get_queue(request):
	return status_info(request)

@jsonrpc_method('raise')
def higher(request, track):
	queue = list(QueueItem.objects.all())[1:]
	for (index,item) in enumerate(queue):
		if item.id == track["id"]:
			if index > 0:
				tmp = queue[index-1].index
				queue[index-1].index = queue[index].index
				queue[index].index = tmp
				queue[index].save()
				queue[index-1].save()
			break

	return status_info(request)

@jsonrpc_method('lower')
def lower(request, track):
	queue = list(QueueItem.objects.all())[1:]
	for (index,item) in enumerate(queue):
		if item.id == track["id"]:
			if index < len(queue)-1:
				tmp = queue[index+1].index
				queue[index+1].index = queue[index].index
				queue[index].index = tmp
				queue[index].save()
				queue[index+1].save()
			break

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
	ret = []
	for item in ChatItem.objects.all()[:limit]:
		msg = {"when":mktime(item.when.timetuple()),"who":item.who, "what":item.what}
		if item.what == "skip":
			msg["track"] = {"url":item.info.url}
			msg["info"] = metadata(item.info)
		else:
			msg["message"] = item.message
		ret.append(msg)
	return ret

@jsonrpc_method('chat')
def chat(request, username, text):
	item = ChatItem(what="says", message=text, who=username)
	item.save()

@jsonrpc_method('get_history')
def get_history(request, limit):
	return chat_history(request, limit)

player = gst.element_factory_make("playbin2", "player")

def next_track():
	QueueItem.current().delete() # remove current first item from queue
	if QueueItem.objects.all().count()>0:
		toplay = QueueItem.current()
		f = cached(toplay.what)
		player.set_property("uri", "file://"+f)
	else:
		global status
		player.set_property("uri", "")
		player.set_state(gst.STATE_NULL)
		if status == Status.playing:
			status = Status.idle

@jsonrpc_method('skip')
def skip(request, username):
	current = QueueItem.current()
	if current != None:
		item = ChatItem(what="skip", info = current.what, who=username)
		item.save()
		current.delete()
	return status_info(request)

def message_handler(bus, message):
	t = message.type
	if t == gst.MESSAGE_EOS:
		print "end of stream"
		next_track()
	
	elif t == gst.MESSAGE_ERROR:
		err, debug = message.parse_error()
		print "error: %s"%err, debug

class Looper(Thread):
	def run(self):
		loop = gobject.MainLoop()
		loop.run()

gobject.threads_init()
loop = Looper()
loop.setDaemon(True)
loop.start()

bus = player.get_bus()
bus.add_signal_watch()
bus.connect("message", message_handler)

def play_current():
	toplay = QueueItem.current()
	f = cached(toplay.what)
	print "toplay", f
	player.set_property("uri", "file://"+f)
	player.set_state(gst.STATE_PLAYING)
	print "player", player

@jsonrpc_method('pause')
def pause(request, shouldPause):
	global status
	if not shouldPause:
		if status == Status.idle and QueueItem.objects.all().count()>0:
			if is_cached(QueueItem.current().what):
				play_current()
			status = Status.playing
		elif status == Status.paused:
			player.set_state(gst.STATE_PLAYING)
			status = Status.playing
	else:
		if status == Status.playing:
			player.set_state(gst.STATE_PAUSED)
			status = Status.paused

	return status_info(request)
