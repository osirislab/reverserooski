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

@client.route('/register', methods=['POST'])
def register_client():
    admin=User.query.filter_by(username="admin").first().id
    try:
        c=Client(
            clientname=request.form['clientname'],
            uname=request.form['uname'],
            registration_time=datetime.utcnow(),
            ownerid=admin,
        )
        c.set_key()
        db.session.add(c)
        db.session.commit()
        return json.dumps([c.id, c.key])
    except IntegrityError as e:
        db.session.rollback()
    #return 'err'

@client.route('/get_pending', methods=['POST'])
def get_pending():
    """
    This is where the client ping us for their
    next set of commands.

    :return json: the pending commands
    """
    return json.dumps(list(map(
        lambda command: command.pending,
        Client.query.filter_by(id=request.form['clientid']).first().commands
    )))

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
    commands=Command.query.filter(
        *(Command.id==c
        for c in report.keys())
    ).all()

    for c in commands:
        c.stdout=report[c.id]
        c.pending=False
    db.session.commit()
    return ''
