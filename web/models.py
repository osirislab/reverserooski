from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta, timezone
from Crypto import Random
from hashlib import sha256

from .app import db


rand=Random.new()


def get_now():
    """
    make EST adjusted datetime object for current time
    """
    return datetime.now(tz=timezone(timedelta(hours=-5)))


def get_random():
    """
    Reads out n bytes from Random object, and
    returns their hex equivilant.
    :param n str: amount of bytes to read
    :return str: n length string of random chars
    """
    return sha256(rand.read(256)).hexdigest()


class struct:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            self.__setattr__(key, val)


class NavItem(struct):
    text=''
    link=''


class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(128), unique=True, index=True)
    password=db.Column(db.String(128), nullable=False)

    def get_id(self):
        return self.username

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Client(db.Model):
    id=db.Column(db.String(32), default=get_random, unique=True, primary_key=True)
    ownerid=db.Column(db.Integer, db.ForeignKey('user.id'))

    clientname=db.Column(db.String(128), unique=False, index=False) #hostname
    uname=db.Column(db.String(128), unique=False, index=False)
    key=db.Column(db.String(128), unique=False, index=False)

    lastping=db.Column(db.DateTime(), default=get_now())
    registration_time=db.Column(db.DateTime, default=get_now())

    owner=db.relationship('User', backref=db.backref('clients', lazy=True))

    def check_key(self, key):
        return check_password_hash(self.key, key)

    def set_key(self):
        self.key=generate_password_hash(get_random())

    def get_pending_commands(self):
        return filter(
            lambda command: command.pending,
            self.commands
        )


class Command(db.Model):
    id=db.Column(db.String(32), default=get_random, unique=True, primary_key=True)
    clientid=db.Column(db.String(32), db.ForeignKey('client.id'))

    command=db.Column(db.String(256), unique=False, index=False)
    pending=db.Column(db.Boolean(), unique=False, index=False)
    stdout=db.Column(db.Text(), unique=False, index=False)

    creation_time=db.Column(db.DateTime(), default=get_now())
    submission_time=db.Column(db.DateTime(), default=None, nullable=True)

    owner=db.relationship('Client', backref=db.backref('commands', lazy=True))

    def check_key(self, key):
        return self.get_client().check_key(key)

    def set_submission(self, stdout, set_pending=True):
        self.pending = True if set_pending else self.pending
        self.stdout=stdout
        self.submission_time=get_now()
