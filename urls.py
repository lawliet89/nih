from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from utils import site_path
from jukebox.jsonrpc import jsonrpc_site
import jukebox.jsonfuncs
import jukebox.configfuncs

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': site_path('jukebox/static'), 'show_indexes': True}),
    (r'^spider$', 'jukebox.views.spider'),
    (r'^config$', 'jukebox.views.config'),
    (r'^$', 'jukebox.views.index'),
    url(r'^rpc/jukebox/browse$', jsonrpc_site.dispatch, name="jsonrpc_browser"),
    url(r'^rpc/jukebox', jsonrpc_site.dispatch, name="jsonrpc_mountpoint"),
)
