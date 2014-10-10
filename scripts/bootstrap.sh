#!/bin/bash
set -e
git submodule update --init --recursive
apt-get install python-pip python-musicbrainz2 python-alsaaudio python-magic python-mysqldb mysql-server python-gst0.1
pip install django==1.3.1 django-nose South mutagen BeautifulSoup django-genshi

python scripts/setupdb.py
echo ""
echo "Bootstrapped successfully"
echo "Run 'python src/manage.py runserver' to start the development server"
