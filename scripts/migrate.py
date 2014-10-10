import os.path
from helpers import sh

def backup(path):
    print "Backing up database to %s" % path
    sql = sh('mysqldump', 'jukebox', '--user=jukebox', '--password=jukebox', '--add-drop-table', '--add-drop-database')
    with open(path, 'w') as f:
        f.write(sql)

def migrate(target):
    backup(os.path.join(target, 'current', 'db-backup.sql'))
    sh('python', 'src/manage.py', 'syncdb')
    sh('python', 'src/manage.py', 'migrate')
