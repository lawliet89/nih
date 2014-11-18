from jsonrpc import jsonrpc_method
from globals import site

from alsaaudio import Mixer, ALSAAudioError

volume_who = ""
volume_direction = ""

def volume():
    try:
        volume = Mixer().getvolume()[0]
    except ALSAAudioError:
        volume = 'Error'
    return {"volume":volume, "who":volume_who, "direction": volume_direction}

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
