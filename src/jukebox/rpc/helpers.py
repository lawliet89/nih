from jukebox.models import QueueItem
from jukebox.cache import albumArt

def metadata(item):
    if not item.got_metadata:
        return None
    ret = { 
        "artistName": item.artist, 
        "albumTitle": item.album, 
        "trackName": item.title, 
        "trackNumber":item.trackNumber, 
        "totalTime": item.trackLength
    }
    if albumArt(item):
        ret["cacheHash"] = item.hash()
    return ret

def reindex_queue():
    index = 0
    for _, item in enumerate(QueueItem.objects.all()):
        item.index = index            
        item.save()
        index += 1
