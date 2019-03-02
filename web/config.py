
import os
class Config():
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@db/revi'
    DOMAIN='https://revi.osiris.cyber.nyu.edu'

    def __init__(self):
        if 'dev.py' in sys.argv:
            self.SECRET_KEY='DEBUG'
            self.SQLALCHEMY_DATABASE_URI = 'sqlite:///.data/db.db'
            self.DOMAIN='http://localhost:5000'
