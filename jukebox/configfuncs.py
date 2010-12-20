from jsonrpc import jsonrpc_method
from models import *

@jsonrpc_method("all_roots")
def all_roots(request):
	ret = []
	for root in WebPath.get_root_nodes():
		ret.append({"url":root.url, "count":MusicFile.objects.filter(url__startswith=root.url).count()})
	return ret

@jsonrpc_method("current_rescans")
def current_rescans(request):
	ret = []
	for root in WebPath.get_root_nodes():
		if WebPath.objects.filter(checked = False).filter(url__startswith=root.url).count()>0:
			ret.append(root.url)
	return ret
