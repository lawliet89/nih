from jsonrpc import jsonrpc_method
from globals import site

from socket import gethostbyaddr

@jsonrpc_method('get_username', site=site)
def get_username(request):
    return request.session.get('username', None)         \
        or str(request.META.get("REMOTE_HOST", ""))      \
        or gethostbyaddr(request.META["REMOTE_ADDR"])[0] \
        or "Unknown"

@jsonrpc_method('set_username', site=site)
def set_username(request, username):
    request.session['username'] = username
    return username

@jsonrpc_method('get_version', site=site)
def get_version(request):
    from jukebox.version import get_version
    return get_version()
