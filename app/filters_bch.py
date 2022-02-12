from app import app
from decimal import *


def convert_bch_to_local(amount, currency):
    """
        Converts BCH to Local currency
    """
    from app import db
    from app.classes.models import btc_cash_Prices
    from app.common.functions import floating_decimals
    getcurrentprice = db.session.query(
        btc_cash_Prices).filter_by(currency_id=currency).first()
    bt = getcurrentprice.price
    z = Decimal(bt) * Decimal(amount)
    c = floating_decimals(z, 2)
    return c


def convert_local_to_bch(amount, currency):
    """
        Converts Local currency to BCH
    """
    from app import db
    from app.classes.models import btc_cash_Prices
    from app.common.functions import floating_decimals
    getcurrentprice = db.session.query(
        btc_cash_Prices).filter_by(currency_id=currency).first()

    bt = getcurrentprice.price
    z = Decimal(amount) / Decimal(bt)
    c = floating_decimals(z, 8)
    return c


@app.template_filter('usd_to_currency_bch')
def usd_to_currency_bch(price, currency):
    """
        Converts 
    """
    from app.classes.models import btc_cash_Prices
    from app import db
    getcurrentprice = db.session.query(
        btc_cash_Prices).filter_by(currency_id=currency).first()
    if currency == 1:
        return price
    else:
        x = Decimal(price) / Decimal(getcurrentprice.price)
        bt = (Decimal(getcurrentprice.price) * x)
        c = '{0:.2f}'.format(bt)
        return c


@app.template_filter('bch_to_currency')
def bch_to_currency(btccashamount, currency):
    """
    Converts the btc amount to users currency 
    """
    from app.classes.models import btc_cash_Prices
    from app import db

    getcurrentprice = db.session.query(btc_cash_Prices) \
        .filter_by(currency_id=currency).first()
    x = Decimal(btccashamount)

    bt = (Decimal(getcurrentprice.price) * x)

    c = '{0:.2f}'.format(bt)
    return c


@app.template_filter('format_to_string_bch')
def format_to_string_bch(value):
    """
    Returns price in proper decimal form so jinja doesnt change it
    """
    def num_after_point(x):
        s = str(x)
        if not '.' in s:
            return 0
        return len(s) - s.index('.') - 1
    num = num_after_point(value)
    if num > 6:
        c = ('%.08f' % (Decimal(value)))
    else:
        c = value
    return c


@app.template_filter('btcprice_btccash_btccash')
def convert_local_to_bch_filter(price, currency):
    from app.classes.models import btc_cash_Prices
    from app import db
    getcurrentprice = db.session.query(btc_cash_Prices) \
        .filter_by(currency_id=currency).first()
    bt = getcurrentprice.price
    z = Decimal(price) / Decimal(bt)
    c = '{0:.8f}'.format(z)
    return c
