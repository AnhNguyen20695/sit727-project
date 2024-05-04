from flask import Flask
from .config import *
from .utils import *
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
db = utilities.MySQL_Database(mode='primary',env=env)
db_read = utilities.MySQL_Database(mode='read',env=env)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
from .note import notes
from .auth import auth

app.register_blueprint(notes, url_prefix='/')
app.register_blueprint(auth, url_prefix='/')