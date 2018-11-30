#!/usr/bin/env python3

from auth import auth_bp, login_required
from flask import Flask, request
from render import render
from Host import Host
import hashlib
import json
import time

app=Flask(__name__)
app.register_blueprint(auth_bp)
app.config.from_mapping(
    SECRET_KEY=b'\xc8L\xb2}\x19\xd0s\xdcB\xb0G\xb7\x93\xb8D\xb3=\x9f\xe1\xeb}{K\x8e'
)
client_text=open('client.sh').read().format(python=open('client.py').read())

hosts=dict() # hostname -> Host


@app.route('/index.html')
def index():
    return render('index.html')

@app.route('/client')
def client():
    return client_text

@app.route('/register_client', methods=['POST'])
def register_client():
    hostname=request.form['hostname']
    uname=request.form['uname']
    if hostname not in hosts:
        hosts[hostname] = Host(hostname, uname)
        return "{\"success\":true}"
    return "{\"success\":false}"

@app.route('/view_host')
def view_pending():
    pass

@app.route('/get_pending', methods=['POST'])
def get_pending():
    hostname=request.form['hostname']
    return json.dumps(hosts[hostname].get_pending())

@app.route('/submit_pending', methods=['POST'])
def submit_pending():
    print(request.form)

@app.route('/control', methods=['POST'])
def control():
    hostname=request.form['hostname']
    uname=request.form['uname']
    host=hosts[hostname]

@app.route('/submit_command', methods=['GET','POST'])
@login_required
def submit_cmd():
    if request.method == "POST":
        hostname=request.form['hostname']
        command=request.form['command']
        hosts[hostname].add_cmd(command)
    return render(
        'submit_command.html',
        hosts=list(hosts.keys())
    )

@app.route('/console')
def console():
    pass

if __name__ == "__main__":
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000
    )
