from django_genshi import render_to_response
from django.conf import settings
from spider import spider
from models import *

def index(request):
    data = { 
        "lastfm_name": settings.LASTFM_USER,
        "repo_url": settings.REPO_URL,
    }
    return render_to_response("index.xml", data)

def spider(request):
	return render_to_response("spider.xml", {"spider": spider})

def config(request):
	return render_to_response("config.xml", {"roots": WebPath.get_root_nodes()})
