from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .app import db

class struct:
    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            self.__setattr__(key, val)

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

class Command(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    clientid=db.Column(db.Integer, unique=False, index=False)
    command=db.Column(db.String(256), unique=False, index=False)
    pending=db.Column(db.Boolean(), unique=False, index=False)
    stdout=db.Column(db.Text(), unique=False, index=False)

    def get_clientid(self):
        return self.clientid

    def get_command(self):
        return self.command

    def get_id(self):
        return self.id

    def set_stdout(self, stdout):
        self.stdout=stdout

class Client(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    clientname=db.Column(db.String(128), unique=False, index=False)
    uname=db.Column(db.String(123), unique=False, index=False)
    registration_time=db.DateTime()

    def get_clientname(self):
        return self.clientname

    def get_id(self):
        return self.id

    def get_all_commands(self):
        return Command.query.filter_by(
            clientid=self.id
        ).all()

    def get_pending_commands(self):
        return Command.query.filter_by(
            clientid=self.id,
            pending=True,
        ).all()

class NavItem(struct):
    text=''
    link=''
