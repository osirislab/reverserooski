from flask import request, redirect, url_for, flash, render_template, Blueprint
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

from .models import ClientTable
from .forms import SubmitCommandForm

from ..models import Client, Command, NavItem
from ..app import db

dashboard = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def get_navitems():
    """
    TODO: Make this cacheable 

    Makes a iterble list of NavItems that will be 
    used in the dashboard template. The NavItems will 
    correspond to each registered client.The NavItem class 
    is defined in reverseroski/reverseroski/models.py.

    :return [ NavItem ]: list of NavItem objects
    """
    clients=Client.query.filter_by().all()
    return [
        NavItem(
            text=client.clientname,
            link="/dashboard/view/{clientid}".format(
                clientid=client.id
            )
        ) for client in clients
    ]

def make_client_table(clientid):
    """
    Makes a table object from client data. Used in the 
    dashboard client view. The table object is used in 
    the dashboard jinja template. The ClientTable class
    is defined in reverseroski/reverseroski/models.py. 
    
    :param int clientid: id number for client
    :return ClientTable: client table object
    """
    client=Client.query.filter_by(id=clientid).first()
    return ClientTable(
        headers=[
            'timestamp',
            'command',
            'pending',
            'stdout',
        ], client=client,
    )

@dashboard.route('/')
@login_required
def serve_dashboard():
    return render_template(
        'dashboard/dashboard.html',
        navitems=get_navitems()
    )

@dashboard.route('/view/<int:clientid>', methods=['GET','POST'])
@login_required
def serve_view(clientid):
    form=SubmitCommandForm()
    if form.validate_on_submit():
        try:
            c=Command(
                clientid=clientid,
                pending=True,
                command=form.command.data,
            )
            db.session.add(c)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash('error adding command to database')
    return render_template(
        'dashboard/view.html',
        navitems=get_navitems(),
        table_data=make_client_table(clientid),
        form=form
    )


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
