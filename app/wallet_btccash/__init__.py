from flask import Blueprint

wallet_btccash = Blueprint('wallet_btccash', __name__)

from . import views