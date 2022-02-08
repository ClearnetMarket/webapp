from app import app
from decimal import *


@app.template_filter('usdtocurrency_btccash')
def usdtocurrency_btccash(price, currency):
    from app.classes.models import btc_cash_Prices
    from app import db
    getcurrentprice = db.session.query(btc_cash_Prices)\
        .filter_by(currency_id=currency).first()
    if currency == 1:
        return price
    else:
        
        x = Decimal(price) / Decimal(getcurrentprice.price)
        bt = (Decimal(getcurrentprice.price) * x)
        c = '{0:.2f}'.format(bt)
        return c


@app.template_filter('btccashtocurrency')
def btccashtocurrency(btccashamount, currency):
    """
    Converts the btc amount to user currency
    """
    from app.classes.models import btc_cash_Prices
    from app import db

    getcurrentprice = db.session.query(btc_cash_Prices) \
        .filter_by(currency_id=currency).first()
    x = Decimal(btccashamount)

    bt = (Decimal(getcurrentprice.price) * x)

    c = '{0:.2f}'.format(bt)
    return c


@app.template_filter('btcprice_btccash_btccash')
def btcprice_btccash(price, currency):
    from app.classes.models import btc_cash_Prices
    from app import db
    getcurrentprice = db.session.query(btc_cash_Prices) \
        .filter_by(currency_id=currency).first()
    bt = getcurrentprice.price
    z = Decimal(price) / Decimal(bt)
    c = '{0:.8f}'.format(z)
    return c


@app.template_filter('currencytocurrency_btccash')
def currencytocurrency_btccash(price, currency, currentusercurrency):
        from app.classes.models import btc_cash_Prices
        from app import db
        getcurrentuserprice = db.session.query(btc_cash_Prices)\
            .filter_by(currency_id=currentusercurrency).first()

        getothercurrency = db.session.query(btc_cash_Prices)\
            .filter_by(currency_id=currency).first()

        b = getcurrentuserprice.price
        c = getothercurrency.price
        x = Decimal(price) / Decimal(b)
        bt = (Decimal(c) * x)
        c = '{0:.2f}'.format(bt)
        return c


@app.template_filter('currencyformat_btccash')
def currencyformat_btccash(id):
    from app import db
    from app.classes.models import Currency
    getfilter = db.session.query(Currency).filter_by(code=id).first()
    return getfilter.symbol


@app.template_filter('otherformatbtctostring_btccash')
def otherformatbtctostring_btccash(value):
    return '%.08f' % value


@app.template_filter('formatbtctostring_btccash')
def formatbtctostring_btccash(value):
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


# def priceaftermargin(margin, currency):
#     getcurrentprice = db.session.query(btcPrices) \
#         .filter_by(currency_id=currency).first()
#     marginq = db.session.query(Query_margin).filter_by(id=margin).first()
#     margin1 = marginq.value
#     bt = getcurrentprice.price
#     z = margin1
#     if 0 > margin1:
#         newprice = (z * -bt)
#         x = (newprice - bt)
#         y = (Decimal(bt) - Decimal(x))
#         c = floating_decimals(y, 2)
#         return c
#     else:
#         y = Decimal(z * bt)
#         c = '{0:.2f}'.format(y)
#         return c



def convertbtctolocal(amount, currency):
    from app import db
    from app.classes.models import btc_cash_Prices
    from app.common.functions import floating_decimals
    getcurrentprice = db.session.query(
        btc_cash_Prices).filter_by(currency_id=currency).first()
    bt = getcurrentprice.price
    z = Decimal(bt) * Decimal(amount)
    c = floating_decimals(z, 2)
    return c


def convertlocaltobtc(amount, currency):
    from app import db
    from app.classes.models import btc_cash_Prices
    from app.common.functions import floating_decimals
    getcurrentprice = db.session.query(
        btc_cash_Prices).filter_by(currency_id=currency).first()

    bt = getcurrentprice.price
    z = Decimal(amount) / Decimal(bt)
    c = floating_decimals(z, 8)
    return c
