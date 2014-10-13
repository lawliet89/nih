from settings import PROJECT_ROOT, REPO_URL
from os import pardir
from os.path import join, isfile

def get_version():
    keys = ['repo', 'hash', 'timestamp']
    path = join(PROJECT_ROOT, pardir, 'VERSION')
    if isfile(path):
        values = [line.strip() for line in open(path)]
    else:
        values = ['unknown' for k in keys]
    d = dict(zip(keys, values))
    d['url'] = '%s/commit/%s' % (REPO_URL, d['hash'])
    return d
        
