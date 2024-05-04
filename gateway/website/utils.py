from functools import wraps
from flask import session, render_template


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kws):
        if not session['loggedin']:
            return render_template("login.html", user=session)
        return f(session, *args, **kws)
    return decorated_function