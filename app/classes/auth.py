# coding=utf-8
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from app import db, login_manager
from datetime import datetime
from uuid import uuid4

def get_uuid():
    return uuid4().hex

class Auth_UserFees(db.Model):
    __tablename__ = 'auth_user_fees'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,
                   unique=True)
    user_id = db.Column(db.INTEGER)
    buyerfee = db.Column(db.DECIMAL(6, 4))
    buyerfee_time = db.Column(db.TIMESTAMP())
    vendorfee = db.Column(db.DECIMAL(6, 4))
    vendorfee_time = db.Column(db.TIMESTAMP())


class Auth_AccountSeedWords(db.Model):
    __tablename__ = 'auth_account_seed_words'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,
                   unique=True)
    user_id = db.Column(db.INTEGER)
    word00 = db.Column(db.VARCHAR(30))
    word01 = db.Column(db.VARCHAR(30))
    word02 = db.Column(db.VARCHAR(30))
    word03 = db.Column(db.VARCHAR(30))
    word04 = db.Column(db.VARCHAR(30))
    word05 = db.Column(db.VARCHAR(30))
    wordstring = db.Column(db.TEXT)


class Auth_User(UserMixin, db.Model):
    __tablename__ = 'auth_users'
    __bind_key__ = 'clearnet'
    __table_args__ = {"schema": "public"}

    id = db.Column(db.Integer,
                   autoincrement=True,
                   primary_key=True,
                   unique=True)
    uuid = db.Column(db.String(32))
    username = db.Column(db.VARCHAR(40))
    password_hash = db.Column(db.TEXT)
    member_since = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    email = db.Column(db.VARCHAR(350))
    wallet_pin = db.Column(db.VARCHAR(5))
    profileimage = db.Column(db.VARCHAR(100))
    stringuserdir = db.Column(db.VARCHAR(100))
    bio = db.Column(db.TEXT)
    country = db.Column(db.VARCHAR(100))
    currency = db.Column(db.INTEGER)
    vendor_account = db.Column(db.INTEGER)
    selling_from = db.Column(db.VARCHAR(100))
    last_seen = db.Column(db.TIMESTAMP(), default=datetime.utcnow())
    admin = db.Column(db.INTEGER)
    admin_role = db.Column(db.INTEGER)
    dispute = db.Column(db.INTEGER)
    fails = db.Column(db.INTEGER)
    locked = db.Column(db.INTEGER)
    vacation = db.Column(db.INTEGER)
    shopping_timer = db.Column(db.TIMESTAMP())
    lasttraded_timer = db.Column(db.TIMESTAMP())
    shard = db.Column(db.INTEGER)
    usernode = db.Column(db.INTEGER)
    affiliate_account = db.Column(db.INTEGER)
    confirmed = db.Column(db.INTEGER)
    passwordpinallowed = db.Column(db.INTEGER)

    def __init__(self,
                 username,
                 password_hash,
                 member_since,
                 email,
                 wallet_pin,
                 profileimage,
                 stringuserdir,
                 bio,
                 country,
                 currency,
                 vendor_account,
                 selling_from,
                 last_seen,
                 admin,
                 admin_role,
                 dispute,
                 fails,
                 locked,
                 vacation,
                 shopping_timer,
                 lasttraded_timer,
                 shard,
                 usernode,
                 affiliate_account,
                 confirmed,
                 passwordpinallowed,
                 ):
        self.username = username
        self.password_hash = password_hash
        self.member_since = member_since
        self.email = email
        self.wallet_pin = wallet_pin
        self.profileimage = profileimage
        self.stringuserdir = stringuserdir
        self.bio = bio
        self.country = country
        self.currency = currency
        self.vendor_account = vendor_account
        self.selling_from = selling_from
        self.last_seen = last_seen
        self.admin = admin
        self.admin_role = admin_role
        self.dispute = dispute
        self.fails = fails
        self.locked = locked
        self.vacation = vacation
        self.shopping_timer = shopping_timer
        self.lasttraded_timer = lasttraded_timer
        self.shard = shard
        self.usernode = usernode
        self.affiliate_account = affiliate_account
        self.confirmed = confirmed
        self.passwordpinallowed = passwordpinallowed

    @staticmethod
    def cryptpassword(password):
        return generate_password_hash(password)

    @staticmethod
    def decryptpassword(pwdhash, password):
        return check_password_hash(pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)

        return s.dumps({'id': self.id}).decode('ascii')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)

        return True

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return Auth_User.query.get(data['id'])


class AnonymousUser(AnonymousUserMixin):
    def __init__(self):
        self.username = 'Guest'


login_manager.anonymous_user = AnonymousUser


db.configure_mappers()
db.create_all()
db.session.commit()
