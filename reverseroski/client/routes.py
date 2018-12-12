from flask import request, redirect, url_for, flash, render_template, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError
from os import urandom
from hashlib import sha256

from .forms import RegisterClientForm
from ..app import db
from ..models import Client, Command

client = Blueprint('client', __name__, url_prefix='/client')


@client.route('/')
def serve_client():
    return open(
        'shell/shell.sh'.format(
            python=open(
                'shell/shell.py'
            ).read()
        )
    ).read()

@client.route('/register', methods=['POST'])
def register_client():
    form = RegisterClientForm()
    if form.validate_on_submit():
        try:
            c=Client(
                clientname=form.clientname.data,
                uname=form.uname.data,
                registration_time=datetime.utcnow(),
            )
            db.session.add(c)
            db.session.commit()
            return json.dumps({
                'hostid':str(c.get_id()),
            })
        except IntegrityError:
            db.session.rollback()
    return ''

@client.route('/get_pending', methods=['POST'])
def get_pending():
    return json.dumps(Command.query.filter_by(
        clientname=form.clientname.data,
        clientid=form.clientid.data,
        pending=True,
    ).all())
