#!/bin/bash
set -e
LOGFILE=/var/log/gunicorn.access.log
LOGDIR=$(dirname $LOGFILE)
NUM_WORKERS=3
# user/group to run as
USER=www-data
GROUP=www-data
SCRIPT_URL=/apps/med
cd /data/webapps/med

test -d $LOGDIR || mkdir -p $LOGDIR
exec /opt/pypy/bin/gunicorn_django -b 127.0.0.1:9000 -w $NUM_WORKERS \
  --user=$USER --group=$GROUP --log-level=debug \
  --log-file=$LOGFILE 2>>$LOGFILE
