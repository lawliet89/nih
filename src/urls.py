from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.conf import settings

from utils import site_path
import jukebox.jsonfuncs
import jukebox.configfuncs

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_path('jukebox/static'), 'show_indexes': True}),
    (r'^cache/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_path(settings.CACHE_FOLDER), 'show_indexes': True}),
    (r'^spider$', 'jukebox.views.spider'),
    (r'^config$', 'jukebox.views.config'),
    (r'^$', 'jukebox.views.index'),
    url(r'^rpc/jukebox/browse$', 'jsonrpc.views.browse', name="jsonrpc_browser", kwargs={"site":jukebox.jsonfuncs.site}),
    url(r'^rpc/jukebox', jukebox.jsonfuncs.site.dispatch, name="jsonrpc_mountpoint"),
    url(r'^rpc/config', jukebox.configfuncs.site.dispatch, name="jsonrpc_mountpoint"),
)
print "opened urls.py"
print jukebox.jsonfuncs.site
