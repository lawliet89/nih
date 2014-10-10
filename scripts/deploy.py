#!/usr/bin/python
import os
import os.path
import shutil

import publish
import filter
import migrate
from helpers import sh

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

def collect_files():
    path = os.path.abspath('target')
    print "Collecting files that need to be deployed into %s" % path
    if os.path.isdir(path):
        shutil.rmtree(path)
    shutil.copytree('.', path, ignore=filter.filter_dir)
    filter.cleanup_dir(path)

def deploy(target, site):
    setup_apache()
    apache('stop')
    migrate.migrate(target)
    collect_files()
    v = publish.make_version(target)
    v.publish(source='target')
    apache_config(target, site)
    apache('start')

    print "\nDeploy completed successfully."
    print "To rollback application: rm -r %s/current; mv %s/previous %s/current" % (target, target, target)
    print "To rollback database: mysql jukebox < %s/previous/db-backup.sql" % target

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Copy files into deploy location and preserves a history of previous publishes')
    parser.add_argument('--target', required=False, default='/usr/share/nih',
        help='The directory to publish files to. Default /usr/share/nih')
    parser.add_argument('--site', required=False, default='nih',
        help='The name of the site in Apache. Default "nih"')
    args = parser.parse_args()

    deploy(args.target, args.site)
