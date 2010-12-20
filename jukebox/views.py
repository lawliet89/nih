from django_genshi import render_to_response
from spider import get_spider
from models import *

def index(request):
	return render_to_response("index.xml")

def spider(request):
	return render_to_response("spider.xml", {"spider": get_spider()})

def config(request):
	return render_to_response("config.xml", {"roots": WebPath.get_root_nodes()})
