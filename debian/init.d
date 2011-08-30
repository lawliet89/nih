#! /bin/sh
### BEGIN INIT INFO
# Provides:          nih
# Required-Start:    $syslog $time $remote_fs
# Required-Stop:     $syslog $time $remote_fs
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Jukebox
# Description:       Debian init script for the nih jukebox
### END INIT INFO

PATH=/bin:/usr/bin:/sbin:/usr/sbin
PIDFILE=/var/run/nih.pid

if [ -f /etc/default/nih ] ; then
	. /etc/default/nih
fi

DAEMON="/usr/share/nih/manage.py runserver 0.0.0.0:$PORT"

. /lib/lsb/init-functions

case "$1" in
  start)
	log_daemon_msg "Starting jukebox" "nih"
	start-stop-daemon -n nih --background --oknodo --exec /usr/bin/python --start -- $DAEMON
	log_end_msg $?
    ;;
  stop)
	log_daemon_msg "Stopping jukebox" "nih"
	killproc -p $PIDFILE $DAEMON
	log_end_msg $?
    ;;
  force-reload|restart)
    $0 stop
    $0 start
    ;;
  status)
    status_of_proc -p $PIDFILE $DAEMON nih && exit 0 || exit $?
    ;;
  *)
    echo "Usage: /etc/init.d/nih {start|stop|restart|force-reload|status}"
    exit 1
    ;;
esac

exit 0
