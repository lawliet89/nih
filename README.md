nih
===

Not Invented Here (a jukebox)

== Deploy ==
* Checkout the source
* sudo scripts/bootstrap.sh
* sudo python scripts/deploy.py

This will create /usr/share/nih, and an Apache site pointing at the most recently deployed version. Default port is 8888, for historical reasons.

To deploy new versions:
* git pull
* sudo python scripts/deploy.py

Each time you run deploy a new timestamped directory will be created in /usr/share/nih. A symlink /usr/share/nih/current always points to the most recent deploy, and /usr/share/nih/previous points to the version before (if any).

To rollback just rm -r current, and rename previous to current. This will rollback the application, as well as the Apache site configuration, but it will not rollback the database. You can do this separtely by running

mysql jukebox < /usr/share/nih/previous/db-backup.sql

Note that if you have already renamed previous to current then the db-backup will now be in current.
