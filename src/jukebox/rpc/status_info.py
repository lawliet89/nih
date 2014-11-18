from jukebox.models import QueueItem
from simple_player import Status
from jukebox.downloader import downloader
from globals import player
from helpers import metadata

def status_info(request):
    objects = QueueItem.objects.all()
    items = [{
        "id": x.id, 
        "url": x.what.url, 
        "username": x.who, 
        "index": x.index } for x in objects]
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
