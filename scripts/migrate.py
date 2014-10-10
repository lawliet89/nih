import os.path
import subprocess
from db_settings import db
from helpers import sh

def _backup(path):
    print "Backing up database to %s" % path
    sql = sh('mysqldump', db.name, 
        '--user=%s' % db.user, 
        '--password=%s' % db.password, 
        '--add-drop-table', '--add-drop-database')
    with open(path, 'w') as f:
        f.write(sql)

def _sync():
    sh('python', 'src/manage.py', 'syncdb')
    sh('python', 'src/manage.py', 'migrate')

def _database_exists():
    try:
        sh('mysql', '-u', db.user, 
            '--password=%s' % db.password, 
            '-e', 'use %s' % db.name)
    except subprocess.CalledProcessError:
        return False
    return True

def migrate(target):
    _backup(os.path.join(target, 'current', 'db-backup.sql'))
    _sync()

def setup_db():
    if _database_exists():
        print 'Database already exists, no need for me to create it.'
    else:
        username = raw_input("Enter your mysql user name (default: root): ") or "root"
        sql = "CREATE DATABASE IF NOT EXISTS %(name)s; GRANT ALL ON %(name)s.* TO '%(user)s' IDENTIFIED BY '%(password)s';" % db
        sh('mysql', '-u', username, '-p' '-f' '-e', sql)
        _sync()
