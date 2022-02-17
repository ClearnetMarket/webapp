from app import app
from decimal import Decimal


@app.template_filter('btctousd')
def btctousd(coinamount):
    from app.classes.wallet_btc import Btc_Prices
    from app import db

    getcurrentprice = db.session.query(Btc_Prices).get(1)
    bt = (Decimal(getcurrentprice.price) * coinamount)
    formatteddollar = '{0:.2f}'.format(bt)
    return formatteddollar


@app.template_filter('btcprice')
def btcprice(price, currency):
    from app.classes.wallet_btc import Btc_Prices
    from app import db
    
    getcurrentprice = db.session\
        .query(Btc_Prices)\
        .filter_by(id=currency)\
        .first()
    bt = getcurrentprice.price
    z = Decimal(price) / Decimal(bt)
    c = '{0:.8f}'.format(z)
    return c


@app.template_filter('currencyformat')
def currencyformat(currencysymbol):
    from app import db
    from app.classes.wallet_btc import Btc_Prices

    getfilter = db.session\
        .query(Btc_Prices)\
        .filter_by(code=currencysymbol)\
        .first()
    return getfilter.symbol


@app.template_filter('btctostring')
def btctostring(value):
    return '%.08f' % value
