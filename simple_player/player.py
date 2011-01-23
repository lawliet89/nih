import pygst
pygst.require("0.10")
import gst
from enum import Enum
import threading
import gobject
from sys import  stderr
from os.path import abspath

class Status(Enum):
	idle = 1
	playing = 2
	paused = 3

class Player:
	def __init__(self, debug = False):
		self.debug = debug
		self._player = gst.element_factory_make("playbin", "player")
		bus = self._player.get_bus()
		bus.add_signal_watch()
		bus.connect("message", self.message_handler)
		self.status = Status.idle

		self.state_lock = threading.Condition()
		self.waiting_for_state_update = False

	def __del__(self):
		with self.state_lock:
			while self.waiting_for_state_update:
				if self.debug:
					print >>stderr, "waiting for update before deletion"
				self.state_lock.wait()

	def message_handler(self, bus, message):
		t = message.type
		if t == gst.MESSAGE_EOS:
			if self.debug:
				print >>stderr, "end of stream"
			self.next_track()
		
		elif t == gst.MESSAGE_ERROR:
			err, debug = message.parse_error()
			if self.debug:
				print >>stderr, "error: %s"%err, debug
		
		elif t == gst.MESSAGE_STATE_CHANGED:
			if message.src == self._player:
				if self.debug:
					print >>stderr, "message from player"
				old, new, pending = message.parse_state_changed()
				if self.debug:
					print >>stderr, "state change", old, new, pending
				if pending == gst.STATE_VOID_PENDING:
					with self.state_lock:
						self._set_internal_state(new)
						if self.waiting_for_state_update:
							self.waiting_for_state_update = False
							self.state_lock.notifyAll()

		return gst.BUS_PASS

	def next_track(self):
		pass

	def elapsed(self):
		if self.status == Status.idle:
			return None
		else:
			(change, current, pending) = self._player.get_state()
			if self.debug:
				print >>stderr, "state", change, current, pending
			if current != gst.STATE_NULL:
				elapsed, format = self._player.query_position(gst.Format(gst.FORMAT_TIME), None)
				return elapsed / gst.SECOND
			else:
				if self.debug:
					print >>stderr, "bad state", current
				return None

	def _set_internal_state(self,state):
		if self.debug:
			print >>stderr, "set internal state for", state
		if state == gst.STATE_NULL:
			self.status = Status.idle
		elif state == gst.STATE_PAUSED:
			self.status = Status.paused
		elif state == gst.STATE_PLAYING:
			self.status = Status.playing
		else:
			raise Exception, state

	def _set_state(self, state):
		with self.state_lock:
			while self.waiting_for_state_update:
				if self.debug:
					print >>stderr, "waiting for update"
				self.state_lock.wait()
		
		(_, current, _) = self._player.get_state()
		if current == gst.STATE_NULL and state == gst.STATE_PAUSED:
			if self.debug:
				print >>stderr, "Can't pause"
		else:
			with self.state_lock:
				kind = self._player.set_state(state)
				if self.debug:
					print >>stderr, "set state result", state, kind
				if kind == gst.STATE_CHANGE_ASYNC:
					self.waiting_for_state_update = True
				elif kind == gst.STATE_CHANGE_SUCCESS:
					self._set_internal_state(state)
				else:
					raise Exception, kind
		
		# gstreamer appears to be partially quantum. measuring state changes results...
		self._player.get_state()

	def stop(self):
		if self.debug:
			print >>stderr, "state: stopping"
			print >>stderr, self._player.get_state()
		self._set_state(gst.STATE_NULL)
		if self.debug:
			print >>stderr, self._player.get_state()

	def pause(self):
		if self.debug:
			print >>stderr, "state: pausing"
			print >>stderr, self._player.get_state()
		self._set_state(gst.STATE_PAUSED)
		if self.debug:
			print >>stderr, self._player.get_state()

	def unpause(self):
		if self.debug:
			print >>stderr, "state: pausing"
			print >>stderr, self._player.get_state()
		self._set_state(gst.STATE_PLAYING)
		if self.debug:
			print >>stderr, self._player.get_state()

	def play(self, path):
		if self.debug:
			print >>stderr, "state: playing"
			print >>stderr, self._player.get_state()
		path = abspath(path)
		self._player.set_property("uri", "file://"+path)
		if self.debug:
			print >>stderr, "state: playing (set uri)"
		self._set_state(gst.STATE_PLAYING)
		if self.debug:
			print >>stderr, "playing", path
			print >>stderr, self._player.get_state()


