from flask import Flask, request
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
        ticket = request.json.get('ticket')#Gets the ticket from the HTML
        user_id = request.json.get('user_id')

        if len(ticket) < 1:
            return {
                'is_success': False,
                'error': 'ticket is too short!'
            }
        else:
            db.execute_query(query=f"""INSERT INTO {APP_DATABASE}.ticket(data,user_id)
                                       VALUES ('{ticket}',{user_id})""",mode='write')
            return {
                'is_success': True,
                'error': 'N'
            }
    if request.method == 'GET':
        print("Got request data: ",request.json)
        user_id = request.json.get('user_id')
        tickets = db_read.execute_query(query=f"""SELECT * FROM {APP_DATABASE}.ticket
                                                WHERE user_id={user_id}""")
        tickets = convert_df_tolist(tickets)
        return {
            'tickets':tickets
        }


@app.route('/delete-ticket', methods=['POST'])
def delete_ticket():
    ticket_id = request.json.get('ticket_id')
    db.execute_query(query=f"""DELETE FROM {APP_DATABASE}.ticket WHERE id={ticket_id}""",mode='write')
    return {
        'is_success': True,
        'message': f'ticket {ticket_id} deleted.'
    }


app.run(host="0.0.0.0", port="5001", debug=True)
db.close_connection()