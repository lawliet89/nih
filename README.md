# nih

Not Invented Here (a jukebox)

## Deploy

* `git clone https://github.com/lshift/nih.git`
* `sudo scripts/bootstrap.sh`
* `sudo python scripts/deploy.py`

This will create `/usr/share/nih`, and an Apache site pointing at the most recently deployed version. Default port is 8888, for historical reasons.

### Deploy an update

To deploy new versions:
* `git pull`
* `sudo python scripts/deploy.py`

Each time you run deploy a new timestamped directory will be created in `/usr/share/nih`. A symlink `/usr/share/nih/current` always points to the most recent deploy, and `/usr/share/nih/previous` points to the version before (if any).

### Rollback a deploy

To rollback just rm -r current, and rename previous to current. This will rollback the application, as well as the Apache site configuration, but it will not rollback the database. You can do this separtely by running

`mysql jukebox < /usr/share/nih/previous/db-backup.sql`

Note that if you have already renamed previous to current then the db-backup will now be in current.

## Develop
* `git clone git@github.com:lshift/nih.git`
* `sudo scripts/bootstrap.sh`

Bootstrap will
* Install dependencies using apt-get and pip (the apt-get stage installs pip, if you don't already have it)
* Create a database and apply migrations to it (you can edit src/db_settings.py to change the database credentials)
* Checkout dependencies that are not available as packages

You can then develop using the Django development server, or deploy to Apache as above
