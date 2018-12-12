from flask import request, redirect, url_for, flash, render_template, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

from ..app import db
from ..models import Client, Command

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard.route('/')
def serve_client():
    return ''

# @client.route('/register', methods=['POST'])
# def register_client():
#     form = RegisterClientForm()
#     if form.validate_on_submit():
#         try:
#             c=Client(
#                 clientname=form.clientname.data,
#                 uname=form.uname.data,
#                 registration_time=datetime.utcnow(),
#             )
#             db.session.add(c)
#             db.session.commit()
#             return json.dumps({
#                 'hostid':str(c.get_id()),
#             })
#         except IntegrityError:
#             db.session.rollback()
#     return ''
