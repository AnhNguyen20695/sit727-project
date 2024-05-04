from flask import Blueprint, render_template, request, flash, jsonify, session
import requests
from . import env
from .config import *
from .utils import login_required
import json

tickets = Blueprint('ticket', __name__)


@tickets.route('/ticket', methods=['GET', 'POST'])
@login_required
def ticket(user_session):
    user_id = session.get('userid')
    conf = HOST_CONFIG[env]
    if request.method == 'POST': 
        ticket = request.form.get('ticket')#Gets the ticket from the HTML

        add_ticket_response = requests.post(f"http://{conf['TICKET_HOST']}:{conf['TICKET_PORT']}/", json={'ticket':ticket, 'user_id':user_id}).json()

        if add_ticket_response.get('is_success'):
            flash('Ticket added!', category='success')
        else:
            flash(add_ticket_response.get('error'), category='error')
    tickets = requests.get(f"http://{conf['TICKET_HOST']}:{conf['TICKET_PORT']}/", json={'user_id':user_id}).json()['tickets']
    return render_template("home.html", user=session, tickets=tickets)


@tickets.route('/delete-ticket', methods=['POST'])
@login_required
def delete_ticket(user_session):  
    ticket = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    ticket_id = ticket['ticketId']
    env = session.get('env')
    conf = HOST_CONFIG[env]
    if ticket:
        del_ticket_response = requests.post(f"http://{conf['TICKET_HOST']}:{conf['TICKET_PORT']}/delete-ticket", json={'ticket_id':ticket_id}).json()
        if del_ticket_response.get('is_success'):
            flash(del_ticket_response.get('message'), category='success')
        else:
            flash('ticket can not be deleted.', category='error')

    return jsonify({})