from django.db import models
from treebeard.mp_tree import MP_Node

class WebPath(MP_Node):
	url = models.URLField()
	node_order_by = ["url"]
	
	def __unicode__(self):
		if self.checked:
			return "Checked url: %s"%self.url
		else:
			return "Unchecked url: %s"%self.url

	checked = models.BooleanField(default=False)
	failed = models.BooleanField(default=False)

class MusicFile(models.Model):
	url = models.URLField()

	def __unicode__(self):
		if self.got_metadata:
			return "Checked url: %s"%self.url
		else:
			return "Unchecked url: %s"%self.url

	failed = models.BooleanField(default=False)
	got_metadata = models.BooleanField(default=False)
	artist = models.CharField(max_length=200)
	album = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	albumArtHash = models.SlugField(blank=True)
	trackLength = models.IntegerField(blank=True, null=True)

class ChatItem(models.Model):
	what = models.CharField(max_length=200)
	when = models.DateTimeField(auto_now_add=True)
	who = models.CharField(max_length=200)

	info = models.ForeignKey('MusicFile', null=True, blank=True)
	message = models.CharField(max_length=1024)

class QueueItem(models.Model):
	who = models.CharField(max_length=200)
	what = models.ForeignKey('MusicFile')
	index = models.FloatField()	

