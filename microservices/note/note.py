from flask import Flask, flash, request
from models import MySQL_Database
from config import *
from utils import *
import utilities
import argparse

parser = argparse.ArgumentParser(
                        prog='ML Web SIT788',
                        description='Workflow',
                        epilog='')

parser.add_argument('-env', '--environment', default='dev',
                    help='Environment to run the app: either dev or prod.')
args = parser.parse_args()
env = args.environment

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
db = utilities.MySQL_Database(mode='primary',env=env)
db_read = utilities.MySQL_Database(mode='read',env=env)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST': 
        note = request.json.get('note')#Gets the note from the HTML
        user_id = request.json.get('user_id')

        if len(note) < 1:
            return {
                'is_success': False,
                'error': 'Note is too short!'
            }
        else:
            db.execute_query(query=f"""INSERT INTO {APP_DATABASE}.note(data,user_id)
                                       VALUES ('{note}',{user_id})""",mode='write')
            return {
                'is_success': True,
                'error': 'N'
            }
    if request.method == 'GET':
        print("Got request data: ",request.json)
        user_id = request.json.get('user_id')
        notes = db_read.execute_query(query=f"""SELECT * FROM {APP_DATABASE}.note
                                                WHERE user_id={user_id}""")
        notes = convert_df_tolist(notes)
        return {
            'notes':notes
        }


@app.route('/delete-note', methods=['POST'])
def delete_note():
    note_id = request.json.get('note_id')
    db.execute_query(query=f"""DELETE FROM {APP_DATABASE}.note WHERE id={note_id}""",mode='write')
    return {
        'is_success': True,
        'message': f'Note {note_id} deleted.'
    }


app.run(host="0.0.0.0", port="5001", debug=True)
db.close_connection()