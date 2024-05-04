from flask import Blueprint, render_template, request, flash, jsonify, session
import requests
from . import env
from .config import *
from .utils import login_required
import json

notes = Blueprint('notes', __name__)


@notes.route('/note', methods=['GET', 'POST'])
@login_required
def note(user_session):
    user_id = session.get('userid')
    conf = HOST_CONFIG[env]
    if request.method == 'POST': 
        note = request.form.get('note')#Gets the note from the HTML

        add_note_response = requests.post(f"http://{conf['NOTE_HOST']}:{conf['NOTE_PORT']}/", json={'note':note, 'user_id':user_id}).json()

        if add_note_response.get('is_success'):
            flash('Note added!', category='success')
        else:
            flash(add_note_response.get('error'), category='error')
    notes = requests.get(f"http://{conf['NOTE_HOST']}:{conf['NOTE_PORT']}/", json={'user_id':user_id}).json()['notes']
    return render_template("home.html", user=session, notes=notes)


@notes.route('/delete-note', methods=['POST'])
@login_required
def delete_note(user_session):  
    note = json.loads(request.data) # this function expects a JSON from the INDEX.js file 
    note_id = note['noteId']
    env = session.get('env')
    conf = HOST_CONFIG[env]
    if note:
        del_note_response = requests.post(f"http://{conf['NOTE_HOST']}:{conf['NOTE_PORT']}/delete-note", json={'note_id':note_id}).json()
        if del_note_response.get('is_success'):
            flash(del_note_response.get('message'), category='success')
        else:
            flash('Note can not be deleted.', category='error')

    return jsonify({})