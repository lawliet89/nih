#!/usr/bin/python
import subprocess
import shutil
from datetime import datetime
import os
import os.path

publish_path_file = ".publish_path"

def expand_path(path):
    from os.path import abspath, expanduser, expandvars
    return abspath(expandvars(expanduser(path)))

def get_git_hash():
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).strip()

def get_git_origin():
    return subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).strip()

def make_version(target):
    return Version(get_git_hash(), get_git_origin(), target)

class Version:
    def __init__(self, version, origin, publish_path):
        self.version = version
        self.origin = origin
        self.timestamp = datetime.now()
        self.publish_path = publish_path
        self.target = os.path.join(publish_path, 'all', self.folder_name())

    def folder_name(self):
        return self.timestamp.strftime('%Y-%m-%d_%H%M%S')

    def publish(self, source="."):
        print "Publishing to %s" % self.target
        self.copy_files(source)
        self.write_metadata()
        self.create_symlink()
        print "Done"

    def copy_files(self, source):
        source = expand_path(source)
        print "Copying files from %s" % source
        shutil.copytree(source, self.target, ignore=shutil.ignore_patterns(('.*')))

    def write_metadata(self):
        print "Writing metadata to VERSION file"
        with open(os.path.join(self.target, 'VERSION'), 'w') as f:
            f.write(self.origin + '\n')
            f.write(self.version + '\n')
            f.write(self.timestamp.isoformat() + '\n')
    
    def create_symlink(self):
        current = os.path.join(self.publish_path, 'current')
        previous = os.path.join(self.publish_path, 'previous')
        if os.path.lexists(previous):
            os.remove(previous)

        if os.path.lexists(current):
            print "Creating symlink to previous version at %s" % previous
            dest = os.readlink(current)
            os.symlink(dest, previous)
            os.remove(current)

        print "Creating symlink at %s" % current
        os.symlink(self.target, current)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Copy files into deploy location and preserves a history of previous publishes')
    parser.add_argument('--source', required=False, default='.', 
        help='The directory to copy files from. Default is the current working directory.')
    parser.add_argument('--target', required=True, 
        help='The directory to publish files to.')
    args = parser.parse_args()

    v = Version(get_git_hash(), get_git_origin(), args.target)
    if os.path.isdir(v.target):
        print '%s already exists' % target
    else:
        v.publish(source=args.source)
