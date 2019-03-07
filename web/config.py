import os
import sys

class Config():
    SECRET_KEY=os.urandom(32)
    DOMAIN='https://revi.osiris.cyber.nyu.edu'

    MYSQL_HOST='db'
    MYSQL_USER='root'
    MYSQL_PASSWORD='password'
    MYSQL_DB='revi'

    SQLALCHEMY_ECHO=True
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SQLALCHEMY_DATABASE_URI=os.environ.pop(
        'SQLALCHEMY_DATABASE_URI',
        default='sqlite:///.data/db/revi.db'
    )

    def __init__(self):
        if 'dev.py' in sys.argv:
            self.SECRET_KEY='DEBUG'
            self.SQLALCHEMY_DATABASE_URI='sqlite:///.data/revi.db'
            self.DOMAIN='http://localhost:5000'
