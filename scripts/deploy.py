#!/usr/bin/python
import subprocess
import os
import os.path
import publish

def sh(*args):
    subprocess.check_output(args)

def setup_apache():
    print "Ensuring apache is installed wth mod_wsgi and mod_headers"
    sh('apt-get', 'install', 'apache2', 'libapache2-mod-wsgi')
    sh('a2enmod', 'headers')

def apache(action):
    print "Alpache: %s" % action
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
    sh('python', 'manage.py', 'syncdb')
    sh('python', 'manage.py', 'migrate')

def deploy(source, target, site):
    setup_apache()
    apache('stop')
    migrate()  
    v = publish.make_version(target)
    v.publish(source=source)
    apache_config(target, site)
    apache('start')

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Copy files into deploy location and preserves a history of previous publishes')
    parser.add_argument('--source', required=False, default='.', 
        help='The directory to copy files from. Default is the current working directory.')
    parser.add_argument('--target', required=False, default='/usr/share/nih',
        help='The directory to publish files to. Default /usr/share/nih')
    parser.add_argument('--site', required=False, default='nih',
        help='The name of the site in Apache. Default "nih"')
    args = parser.parse_args()

    deploy(args.source, args.target, args.site)
