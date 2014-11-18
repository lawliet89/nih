from jsonrpc import jsonrpc_method
from globals import site

from jukebox.models import MusicFile
from helpers import metadata
from random import sample

@jsonrpc_method('search', site=site)
def search(request, inp, count=0, skip=0):
    items = MusicFile.objects
    for term in inp:
        items = items.filter(url__icontains=term)
    items = items.order_by('parent__url', 'url')
    if count > 0:
        items = items[skip:count]
    return [{"url": x.url, "info": metadata(x)} for x in items]

@jsonrpc_method('randomtracks', site=site)
def randomtracks(request, count):
    items = MusicFile.objects.all()
    count = min(count, items.count())
    ret = [{"url":items[x].url} for x in sample(range(items.count()),count)]
    return ret
