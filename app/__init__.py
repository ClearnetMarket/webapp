# coding=utf-8

from flask import Flask, request, render_template, redirect, url_for
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
from flask_qrcode import QRcode
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import sessionmaker
from werkzeug.routing import BaseConverter
from flask_wtf import \
    CSRFProtect, \
    csrf
from flask_paranoid import Paranoid
from time import strftime
import traceback
from config import \
    UPLOADED_FILES_DEST, \
    UPLOADED_FILES_ALLOW, \
    MAX_CONTENT_LENGTH, \
    SQLALCHEMY_DATABASE_URI_0, \
    SECRET_KEY, \
    WTF_CSRF_ENABLED,\
    DEBUG

app = Flask(__name__,
            static_url_path='',
            static_folder='static',
            template_folder='templates')


app.config.from_object('config')
Session = sessionmaker()


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


@app.errorhandler(500)
def internal_error500():
    return render_template('/errors/500.html')


@app.errorhandler(502)
def internal_error502(error):
    app.logger.error(error)
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    app.logger.error('%s %s %s %s %s 5xx 500 ERROR\n%s',
                     ts,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)
    return render_template('/errors/500.html')


@app.errorhandler(404)
def internal_error404(error):
    app.logger.error(error)
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    app.logger.error('%s %s %s %s %s 5xx 404 ERROR\n%s',
                     ts,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)
    return render_template('errors/400.html')


@app.errorhandler(401)
def internal_error404(error):
    app.logger.error(error)
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    app.logger.error('%s %s %s %s %s 5xx 404 ERROR\n%s',
                     ts,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)
    return render_template('errors/401.html')


@app.errorhandler(400)
def internal_error400(error):
    app.logger.error(error)
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    app.logger.error('%s %s %s %s %s 5xx 404 ERROR\n%s',
                     ts,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)
    return render_template('errors/400.html')


@app.errorhandler(413)
def to_large_file(error):
    app.logger.error(error)
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    app.logger.error('%s %s %s %s %s 5xx 413 ERROR\n%s',
                     ts,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)
    return render_template('errors/413.html')


@app.errorhandler(403)
def internal_error403(error):
    app.logger.error(error)
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    app.logger.error('%s %s %s %s %s 5xx 403 ERROR\n%s',
                     ts,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)
    return render_template('errors/403.html')


@app.errorhandler(405)
def internal_error(error):
    app.logger.error(error)
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    app.logger.error('%s %s %s %s %s 5xx 405 ERROR\n%s',
                     ts,
                     request.remote_addr,
                     request.method,
                     request.scheme,
                     request.full_path,
                     tb)
    return render_template('errors/405.html')


@csrf.CSRFError
def csrf_error():
    return render_template('404.html'), 400



# FILTERS
from app import filters_btc_cash, filters_filtersstuff

# regular filters
app.jinja_env.filters['maincatname'] = filters_filtersstuff.maincatname
app.jinja_env.filters['orderpicture'] = filters_filtersstuff.orderpicture
app.jinja_env.filters['cancelwhy'] = filters_filtersstuff.cancelwhy
app.jinja_env.filters['returnwhy'] = filters_filtersstuff.returnwhy
app.jinja_env.filters['adminusername'] = filters_filtersstuff.adminusername
app.jinja_env.filters['achievementdescription'] = filters_filtersstuff.achievementdescription
app.jinja_env.filters['achievementtitle'] = filters_filtersstuff.achievementtitle
app.jinja_env.filters['trustlevel'] = filters_filtersstuff.trustlevel
app.jinja_env.filters['profilepicture'] = filters_filtersstuff.profilepicture
app.jinja_env.filters['username'] = filters_filtersstuff.username
app.jinja_env.filters['buyorsell'] = filters_filtersstuff.buyorsell
app.jinja_env.filters['countryformat'] = filters_filtersstuff.countryformat
app.jinja_env.filters['carrierformat'] = filters_filtersstuff.carrierformat
app.jinja_env.filters['userrating'] = filters_filtersstuff.userrating
app.jinja_env.filters['avgvendorrating'] = filters_filtersstuff.avgvendorrating
app.jinja_env.filters['vendorratingcount'] = filters_filtersstuff.vendorratingcount
app.jinja_env.filters['vendorratingonorder'] = filters_filtersstuff.vendorratingonorder
app.jinja_env.filters['userrating'] = filters_filtersstuff.userrating
app.jinja_env.filters['avguserrating'] = filters_filtersstuff.avguserrating
app.jinja_env.filters['marginpercent'] = filters_filtersstuff.marginpercent



# BTC_Cash FILTERS

app.jinja_env.filters['btccashtocurrency'] = filters_btc_cash.btccashtocurrency
app.jinja_env.filters['formatbtctostring_btccash'] = filters_btc_cash.formatbtctostring_btccash
app.jinja_env.filters['otherformatbtctostring_btccash'] = filters_btc_cash.otherformatbtctostring_btccash
app.jinja_env.filters['currencyformat_btccash'] = filters_btc_cash.currencyformat_btccash
app.jinja_env.filters['btcprice_btccash'] = filters_btc_cash.btcprice_btccash
app.jinja_env.filters['currencytocurrency_btccash'] = filters_btc_cash.currencytocurrency_btccash
app.jinja_env.filters['usdtocurrency_btccash'] = filters_btc_cash.usdtocurrency_btccash


# configuration
app.url_map.converters['regex'] = RegexConverter
app.config['UPLOADED_FILES_DEST'] = UPLOADED_FILES_DEST
app.config['UPLOADED_FILES_ALLOW'] = UPLOADED_FILES_ALLOW
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = SECRET_KEY
app.config['CSRF_ENABLED'] = WTF_CSRF_ENABLED
app.config['DEBUG'] = DEBUG

Session.configure(bind=SQLALCHEMY_DATABASE_URI_0)
paranoid = Paranoid(app)
db = SQLAlchemy(app)
qrcode = QRcode(app)
csrf = CSRFProtect(app)
moment = Moment(app)
mail = Mail(app)


login_manager = LoginManager(app)
login_manager.session_protection = None

login_manager.anonymous_user = "Guest"
paranoid.redirect_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id):
    from app.classes.auth import User
    x = db.session.query(User).filter(User.id == int(user_id)).first()
    return x


# link locations
from .main import main as main_blueprint
app.register_blueprint(main_blueprint, url_prefix='/main')

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

from .vendor import vendor as vendor_blueprint
app.register_blueprint(vendor_blueprint, url_prefix='/vendor')

from .search import search as search_blueprint
app.register_blueprint(search_blueprint, url_prefix='/search')

from .item import item as item_blueprint
app.register_blueprint(item_blueprint, url_prefix='/item')

from .service import service as service_blueprint
app.register_blueprint(service_blueprint, url_prefix='/service')

from .category import category as category_blueprint
app.register_blueprint(category_blueprint, url_prefix='/category')

from .userdata import userdata as userdata_blueprint
app.register_blueprint(userdata_blueprint, url_prefix='/info')

from .message import message as message_blueprint
app.register_blueprint(message_blueprint, url_prefix='/message')

from .profile import profile as profile_blueprint
app.register_blueprint(profile_blueprint, url_prefix='/profile')


from .affiliate import affiliate as affiliate_blueprint
app.register_blueprint(affiliate_blueprint, url_prefix='/affiliate')

from .promote import promote as promote_blueprint
app.register_blueprint(promote_blueprint, url_prefix='/promote')


# btc cash wallet
from app.wallet_btccash import wallet_btccash as wallet_btccash_blueprint
app.register_blueprint(wallet_btccash_blueprint, url_prefix='/bch')


db.configure_mappers()
db.create_all()
db.session.commit()
