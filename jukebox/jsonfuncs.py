from jsonrpc import jsonrpc_method
from jsonrpc.site import JSONRPCSite
from models import *
from time import mktime, strftime, gmtime
from urllib import unquote
from random import sample
from alsaaudio import Mixer
from cache import cached, albumArt
from threading import Thread
from simple_player import Player, Status
import gobject
from utils import registerStartupTask
from os.path import join
import audioscrobbler
from django.conf import settings
from downloader import downloader
from socket import gethostbyaddr

site = JSONRPCSite()
audioscrobbler.enc = "utf8"
post = audioscrobbler.AudioScrobblerPost(username=settings.LASTFM_USER, password=settings.LASTFM_PASSWORD, verbose=True)

@jsonrpc_method('get_caller_hostname', site=site)
def hostname(request):
	if "REMOTE_HOST" in request.META.keys() and request.META["REMOTE_HOST"] != None:
		return str(request.META["REMOTE_HOST"])
	else:
		return gethostbyaddr(request.META["REMOTE_ADDR"])[0]

def metadata(item):
	if not item.got_metadata:
		return None
	ret = {"artistName":item.artist, "albumTitle":item.album, "trackName":item.title, "trackNumber":item.trackNumber, "totalTime": item.trackLength}
	if albumArt(item):
		ret["cacheHash"] = item.hash()
	return ret

def status_info(request):
	objects = QueueItem.objects.all()
	items = [{"id":x.id, "url":x.what.url, "username":x.who} for x in objects]
	itemsMeta = [metadata(x.what) for x in objects]
	if len(items)>0:
		first = (items[0], itemsMeta[0])
	else:
		first = (None, None)

	elapsed = player.elapsed()
	current = QueueItem.current()
	if current!=None and current.what in downloader.downloads():
		state = "caching"
	else:
		state = player.status.name()

	return {
		"status":state,
		"entry":first[0],
		"info": first[1],
		"queue": items[1:],
		"queueInfo": itemsMeta[1:],
		"paused": player.status != Status.playing,
		"elapsedTime": elapsed,
		"downloads": [x.url for x in downloader.downloads()]
	}

@jsonrpc_method('search', site=site)
def search(request, inp):
	items = MusicFile.objects
	for term in inp:
		items = items.filter(url__icontains=term)
	items = items.order_by('parent__url', 'url')
	return [{"url":x.url} for x in items]

@jsonrpc_method('randomtracks', site=site)
def randomtracks(request, count):
	items = MusicFile.objects.all()
	count = min(count, items.count())
	ret = [{"url":items[x].url} for x in sample(range(items.count()),count)]
	return ret

@jsonrpc_method('enqueue', site=site)
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

@jsonrpc_method('dequeue', site=site)
def dequeue(request, username, track):
	queue = list(QueueItem.objects.all())[1:]
	for item in queue:
		if item.id == track["id"]:
			item.delete()
	return status_info(request)

@jsonrpc_method('clear_queue', site=site)
def clear_queue(request, username):
	queue = list(QueueItem.objects.all())[1:]
	for item in queue:
		item.delete()
	return status_info(request)

@jsonrpc_method('get_queue', site=site)
def get_queue(request):
	return status_info(request)

@jsonrpc_method('raise', site=site)
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

@jsonrpc_method('lower', site=site)
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

@jsonrpc_method('get_volume', site=site)
def get_volume(request):
	return volume()

@jsonrpc_method('set_volume', site=site)
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
		elif item.what == "failed":
			msg["error"] = "Failed to download %s"%item.info.url
		else:
			msg["message"] = item.message
		ret.append(msg)
	return ret

@jsonrpc_method('chat', site=site)
def chat(request, username, text):
	item = ChatItem(what="says", message=text, who=username)
	item.save()

@jsonrpc_method('get_history', site=site)
def get_history(request, limit):
	return chat_history(request, limit)

def next_track():
	if QueueItem.objects.all().count()>0:
		QueueItem.current().delete() # remove current first item from queue
		player.stop()
	if QueueItem.objects.all().count()>0:
		play_current()
	elif player.status != Status.idle:
		player.stop()

player = Player()
player.next_track = next_track

@jsonrpc_method('skip', site=site)
def skip(request, username):
	current = QueueItem.current()
	if current != None:
		item = ChatItem(what="skip", info = current.what, who=username)
		item.save()
		print "saved item"
		next_track()
	return status_info(request)

class Looper(Thread):
	def run(self):
		loop = gobject.MainLoop()
		loop.run()

gobject.threads_init()
registerStartupTask(Looper)

def play_current():
	toplay = QueueItem.current()
	f = cached(toplay.what)
	print "toplay", f
	if f != None:
		player.play(f)
		song = toplay.what
		track = dict(artist_name=song.artist,
                 song_title=song.title,
                 length=int(song.trackLength),
				 date_played=strftime("%Y-%m-%d %H:%M:%S", gmtime()), 
                 album=song.album,
                 mbid=""
                )
		print "track", track
		post(**track)
	else:
		player.stop()

@jsonrpc_method('pause', site=site)
def pause(request, shouldPause):
	if not shouldPause:
		if player.status == Status.idle and QueueItem.objects.count()>0:
			from cache import is_cached
			if is_cached(QueueItem.current().what):
				play_current()
		elif player.status == Status.paused:
			player.unpause()
	else:
		if player.status == Status.playing:
			player.pause()

	return status_info(request)
