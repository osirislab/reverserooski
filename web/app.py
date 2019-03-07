#!/usr/bin/env python3

from flask import Flask, request, abort, render_template, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy

from .config import Config

app=Flask(__name__,static_url_path='/static')

app.config.from_object(Config())

Bootstrap(app)
db = SQLAlchemy(app)

from .auth import auth
app.register_blueprint(auth)

from .client import client
app.register_blueprint(client)

from .dashboard import dashboard
app.register_blueprint(dashboard)

@app.route('/')
@login_required
def index():
    return render_template('index.html')

