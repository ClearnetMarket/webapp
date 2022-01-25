from flask_login import current_user
from flask import redirect, url_for, request
from app import db
from functools import wraps
from app.classes.auth import User
from app.classes.admin import websiteOffline
from datetime import datetime


def ADMINaccount_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin == 0:
            return redirect(url_for('index', next=request.url))
        else:
            pass
        return f(*args, **kwargs)
    return decorated_function


def ADMINaccountlevel3_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin_role >= 3:
            pass
        else:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def ADMINaccountlevel4_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin_role >= 4:
            pass
        else:
            return redirect(url_for('index', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def ADMINaccountlevel10_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.admin_role >= 10:
            pass
        else:
            return redirect(url_for('index', next=request.url))

        return f(*args, **kwargs)
    return decorated_function


def ping_user(f):
    @wraps(f)
    def decorated_function_ping(*args, **kwargs):
        if current_user.username is 'Guest':
            pass
        else:
            now = datetime.utcnow()
            user = db.session.query(User).filter_by(username=current_user.username).first()
            user.last_seen = now
            db.session.add(user)
            db.session.commit()
        return f(*args, **kwargs)
    return decorated_function_ping


def website_offline(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        status = db.session.query(websiteOffline).filter_by(id=1).first()
        if status.webstatus == 0:
            pass
        elif status.webstatus == 1:
            return redirect(url_for('main.scheduledmaintenance'))
        elif status.webstatus == 2:
            return redirect(url_for('main.offline'))
        elif status.webstatus == 3:
            return redirect(url_for('main.busy'))
        else:
            pass
        return f(*args, **kwargs)
    return decorated_function


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.username is 'Guest':
            return redirect(url_for('auth.login', next=request.url))
        else:
            pass
        if current_user.is_authenticated:
            pass
        else:
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)

    return decorated_function


def vendoraccount_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.vendor_account == 1:
            pass
        else:
            return redirect(url_for('index', next=request.url))

        return f(*args, **kwargs)
    return decorated_function