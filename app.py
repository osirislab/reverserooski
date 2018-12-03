#!/usr/bin/env python3

from Host import Host, Hosts # load_state, dump_state
from auth import auth_bp, login_required
from flask import Flask, request
from threading import Lock
from render import render
import hashlib
import random
import json
import time
import sys
import art

registration_lock=Lock()

app=Flask(__name__,static_url_path='/static')
app.register_blueprint(auth_bp)
app.config.from_mapping(
    SECRET_KEY=b'\xc8L\xb2}\x19\xd0s\xdcB\xb0G\xb7\x93\xb8D\xb3=\x9f\xe1\xeb}{K\x8e'
)
client_text=open('client.sh').read().format(python=open('client.py').read())

hosts=Hosts() # hostid -> Host


@app.route('/client')
def client():
    return client_text


@app.route('/register_client', methods=['POST'])
def register_client():
    hostname=request.form['hostname']
    uname=request.form['uname']
    print(art.plus, 'registering client {}'.format(hostname))
    registration_lock.acquire()
    hostid=len(hosts)
    hosts.set(Host(hostid, hostname, uname), new=True)
    registration_lock.release()
    return json.dumps({
        'success':True,
        'hostid':hostid,
    })


@app.route('/get_pending', methods=['POST'])
def get_pending():
    hostid=int(request.form['hostid'])
    return json.dumps({'cmds':hosts.get(hostid).get_pending()})


@app.route('/')
@app.route('/home')
@login_required
def index():
    return render('index.html')


@app.route('/view_host/<hostid>')
@login_required
def view_host(hostid):
    return render(
        'view_host.html',
        host=hosts.get(hostid)
    )



@app.route('/submit_pending', methods=['POST'])
@login_required
def submit_pending():
    hostid=request.form['hostid']
    command_data=json.loads(request.form['command_data'])
    try:
        for commandid, stdout in command_data:
            hosts.get(hostid).submit_pending_command(commandid, stdout)
        return '{"success":true}'
    except AssertionError:
        return '{"success":false}'


@app.route('/control', methods=['POST'])
@login_required
def control():
    hostname=request.form['hostname']
    uname=request.form['uname']
    host=hosts.get(hostname)
    return 'error'

@app.route('/submit_command', methods=['GET','POST'])
@login_required
def submit_cmd():
    if request.method == "POST":
        command=request.form['command']
        hostid=request.form['hostid']
        hosts.get(hostid).add_command(command)
    return render(
        'submit_command.html',
        hosts=hosts
    )

@app.route('/console')
def console():
    pass

if __name__ == "__main__":
    app.run(
#        debug=True,
        host='0.0.0.0',
        port=5000
    )
