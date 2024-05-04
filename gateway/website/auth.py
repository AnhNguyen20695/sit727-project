from flask import Blueprint, render_template, request, flash, redirect, url_for, session
import requests
from . import db, db_read
from . import env
from .config import *
from .utils import *


auth = Blueprint('auth', __name__)

@auth.route('/', methods=['GET'])
def home():
    is_loggedin = session.get('loggedin')
    if is_loggedin:
        user_id = session.get('userid')
        conf = HOST_CONFIG[env]
        notes = requests.get(f"http://{conf['NOTE_HOST']}:{conf['NOTE_PORT']}/", json={'user_id':user_id})
        notes = notes.json()['notes']
        return render_template("home.html", user=session, notes=notes)
    else:
        return redirect("/login")

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print("Input email: ",email)

        user = db_read.execute_query(query=f"""SELECT *
                                      FROM {APP_DATABASE}.user
                                      WHERE email='{email}'""").head(1)
        print("Got user: ",user)
        if len(user) > 0:
            if user["password"][0] == password:
                flash('Logged in successfully!', category='success')
                session['loggedin'] = True
                session['userid'] = str(user['id'][0])
                session['username'] = user['first_name'][0]
                session['email'] = user['email'][0]
                return redirect("/")
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=session)


@auth.route('/logout')
def logout():
    session["loggedin"] = False
    session.pop('username', None)
    session.pop('email', None)
    session.pop('userid', None)
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = db_read.execute_query(query=f"""SELECT *
                                      FROM {APP_DATABASE}.user
                                      WHERE email='{email}'""")
        if len(user) > 0:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            create_user_result = db.execute_query(query=f"""INSERT INTO {APP_DATABASE}.user(email, password, first_name)
                                                            VALUES ('{email}', '{password1}', '{first_name}')""",mode="write")
            new_user = db_read.execute_query(query=f"""SELECT *
                                                        FROM {APP_DATABASE}.user
                                                        WHERE email='{email}'""").head(1)
            session['loggedin'] = True
            session['userid'] = str(new_user['id'][0])
            session['username'] = new_user['first_name'][0]
            session['email'] = new_user['email'][0]
            flash('Account created!', category='success')
            return redirect(url_for('notes.note'))

    return render_template("sign_up.html", user=session)