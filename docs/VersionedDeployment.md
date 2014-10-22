# Deployment
The deploy script is designed to make sure that all the state of the jukebox is backed up and every step, and can easily be rolled back: So the source code, the Apache configuration, and the database state. Steps on how to deploy and rollback are found at [README](../README.md). This document is about how it works under the hood.

## Versions
If you use the included deploy script (`scripts/deploy.py`) then your application will have the following structure:
<pre>/usr/bin/nih/
             current/
             previous/
             all/
                 2014-10-22_154628/
                 2014-10-23_112356/
                 2014-11-02_091005/
</pre>

You may have changed the directory from `/usr/bin/nih` by passing parameters to the deploy script.

Every time you run `deploy.py` a new timestamped subdirectory is created in `all`. We will call these directories 'versions'. `current` is a soft link to the most recently created version. `previous` will exist from the second deploy onwards, and is a soft link that points to the last but one version. (Of course, if you rollback by manually manipulating the links, then those invariants will no longer hold.)

### Version structure
Each version has this structure:
<pre>apache.conf
src/
VERSION</pre>

`src` contains the main Django application, and is hosted by Apache using mod_wsgi. Although mod_wsgi, when properly configured, should not serve files indiscriminately from `src`, we try to keep files that must not be exposed over the web outside of `src` where possible, in case of misconfiguration. For that reason `apache.conf` lives at this level, outside of `src`.

### VERSION file format
There is also the `VERSION` file. This file's format is part of nih's public API, and should hopefully never change. It is as follows:
1. First line is the full URL of the repository that your repository was cloned from. "By your repository", I mean the repository that the source was deployed from.
2. Second line is an abitrary string that identifies the version uniquely. In deploy.py this is the git commit hash, but that's not required for this file's format.
3. Third line is the timestamp of when the deploy was run, in [ISO 8601|http://en.wikipedia.org/wiki/ISO_8601] format.

Parsers for this file should not make any assumptions about lines beyond line 3, as these are reserved for adding more metadata in the future.

## Apache
The deploy script creates `nih.conf` in Apache's `sites-available` and `sites-enabled`. In both cases, these are soft links that eventually resolve to `/usr/share/nih/current/apache.conf`. This means that if a new version of the code makes a change to the Apache configuration, these changes can also be rolled back as part of the normal mechanism.

## MySQL
The deploy script also backs up the MySQL database to an SQL file using `mysqldump`. This is placed in the version folder for the *previous* version. If there isn't a previous version (e.g. because this is the first deploy) the file is output to the working directory.
