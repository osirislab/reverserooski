#!/usr/bin/env python3

from flask import Flask, request, abort, render_template, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy

from .config import Config

app=Flask(__name__,static_url_path='/static')

app.config.from_object(Config)

Bootstrap(app)
db = SQLAlchemy(app)


from .auth import auth
from .client import client
from .dashboard import dashboard
app.register_blueprint(auth)
app.register_blueprint(client)
app.register_blueprint(dashboard)

@app.route('/')
@login_required
def index():
    return render('index.html')




'''
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
    pending=hosts.get(hostid).get_pending()
    print(pending)
    return json.dumps({'cmds':pending})



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

'''
