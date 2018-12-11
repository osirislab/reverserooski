from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from .app import db
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True)
    password = db.Column(db.String(128), nullable=False)
    def get_id(self):
        return self.username
    def set_password(self, password):
        self.password = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password, password)
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uploader = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    orig_path = db.Column(db.String(4095))
    thumb_path = db.Column(db.String(4095))
    user = db.relationship('User', backref=db.backref('images'))