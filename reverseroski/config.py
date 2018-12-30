import os

class Config():
    #SECRET_KEY = os.urandom(32)
    SECRET_KEY='1337'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///data/db.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
