set -e
apt-get install apache2 libapache2-mod-wsgi
a2enmod headers

/etc/init.d/apache2 stop
target='/etc/apache2/sites-available/nih.conf'
link='/etc/apache2/sites-enabled/nih.conf'
cp ./scripts/apache-site-config $target
set +e; rm $link; set -e
ln -s $target $link

python manage.py syncdb
python manage.py migrate
./scripts/publish.py --target /usr/share/nih
/etc/init.d/apache2 start
