from jukebox.models import *
from django.contrib import admin
from treebeard.admin import TreeAdmin

class WebPathAdmin(TreeAdmin):
	search_fields = ["url"]

admin.site.register(WebPath, WebPathAdmin)
admin.site.register(MusicFile)
admin.site.register(QueueItem)
admin.site.register(ChatItem)
