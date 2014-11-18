from threading import Thread
import gobject
from utils import registerStartupTask

# The methods exposed via JSON RPC are imported here:
from rpc.search import search, randomtracks
from rpc.misc import get_username, set_username, get_version
from rpc.queue import enqueue, dequeue, clear_queue, get_queue, reorder
from rpc.volume import get_volume, set_volume
from rpc.chat import chat, get_history
from rpc.player import skip, pause
from rpc.globals import site, player

class Looper(Thread):
    def run(self):
        loop = gobject.MainLoop()
        loop.run()

gobject.threads_init()
registerStartupTask(Looper)

