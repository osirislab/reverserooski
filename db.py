import sqlite3
import os

DB_NAME='users.db'

def get_db():
    return sqlite3.connect(DB_NAME)
