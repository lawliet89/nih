#!/usr/bin/python
import subprocess
import os
import os.path
import shutil
import publish
import re

def sh(*args):
    subprocess.check_output(args)

def setup_apache():
    print "Ensuring apache is installed wth mod_wsgi and mod_headers"
    sh('apt-get', 'install', '-y', 'apache2', 'libapache2-mod-wsgi')
    sh('a2enmod', 'headers')

def apache(action):
    print "Apache: %s" % action
    sh('/etc/init.d/apache2', action)

def apache_config(target, site):
    target = os.path.join(target, 'current', 'apache.conf')
    available = '/etc/apache2/sites-available/%s.conf' % site
    enabled = '/etc/apache2/sites-enabled/%s.conf' % site
    print "Deploying changes to apache site configuration. (See %s)." % enabled

    for l in [available, enabled]:
        if os.path.lexists(l):
            os.remove(l)
    os.symlink(target, available)
    os.symlink(available, enabled)

def migrate():
    sh('python', 'src/manage.py', 'syncdb')
    sh('python', 'src/manage.py', 'migrate')

patterns = [
    r"\.py$",
    r"\.xml$",
    r"^src/my.cnf$",
    r"templates/.+\.xml",
    r"jukebox/static/.+\.(js|css|ico|png|jpg|jpeg|gif|xcf)"
]
def keep(path, file):
    if file[0] == '.':
        #print "Ignoring %s. It is hidden" % path
        return False
    if os.path.isdir(path):
        #print "Keeping %s. It is a dir" % path
        return True
    for p in patterns:
        if re.search(p, path):
            #print "Keeping %s. It matches %s" % (path, p)
            return True
    #print "Discarding %s. It didn't match any patterns." % path
    return False

def ignore(dir, files):
    result = []
    for file in files:
        path = os.path.join(dir, file)
        if not keep(path, file):
            result.append(file)
    return result

def collect_files():
    path = os.path.abspath('target')
    print "Collecting files that need to be deployed into %s" % path
    if os.path.isdir(path):
        shutil.rmtree(path)
    shutil.copytree('src', os.path.join(path, 'src'), ignore=ignore)
    shutil.copy('apache.conf', os.path.join(path, 'apache.conf'))

def deploy(target, site):
    setup_apache()
    apache('stop')
    migrate()
    collect_files()
    v = publish.make_version(target)
    v.publish(source='target')
    apache_config(target, site)
    apache('start')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Copy files into deploy location and preserves a history of previous publishes')
    parser.add_argument('--target', required=False, default='/usr/share/nih',
        help='The directory to publish files to. Default /usr/share/nih')
    parser.add_argument('--site', required=False, default='nih',
        help='The name of the site in Apache. Default "nih"')
    args = parser.parse_args()

    deploy(args.target, args.site)
