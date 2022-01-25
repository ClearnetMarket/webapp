import os
from app import db
from app.classes.models import btc_cash_Prices, Query_margin
import random
import string
from decimal import Decimal


def genericprofile(path):
    userid = str(path)
    cmd = 'cp /home/clearnet_webapp/info/user/user-unknown.png /home/info/user/' + userid
    try:
        os.system(cmd)
    except OSError:  # Python >2.7
        pass


def mkdir_p(path):
    try:
        os.makedirs(path, 0o755)
    except OSError:  # Python >2.7
        if os.path.isdir(path):
            pass
        else:
            raise


def itemlocation(x):
    if 1 <= x <= 10000:
        return '1'
    elif 10001 <= x <= 20000:
        return '2'
    elif 20001 <= x <= 30000:
        return '3'
    elif 30001 <= x <= 40000:
        return '4'
    elif 40001 <= x <= 50000:
        return '5'
    elif 50001 <= x <= 60000:
        return '6'
    elif 60001 <= x <= 70000:
        return '7'
    elif 70001 <= x <= 80000:
        return '8'
    elif 80001 <= x <= 90000:
        return '9'
    elif 90001 <= x <= 100000:
        return '10'
    elif 100001 <= x <= 110000:
        return '11'
    elif 110001 <= x <= 120000:
        return '12'
    elif 120001 <= x <= 130000:
        return '13'
    elif 130001 <= x <= 140000:
        return '14'
    elif 140001 <= x <= 150000:
        return '15'
    elif 150001 <= x <= 160000:
        return '16'
    elif 160001 <= x <= 170000:
        return '17'
    elif 170001 <= x <= 180000:
        return '18'
    elif 180001 <= x <= 190000:
        return '19'
    elif 190001 <= x <= 200000:
        return '20'
    elif 200001 <= x <= 210000:
        return '21'
    elif 210001 <= x <= 220000:
        return '22'
    elif 220001 <= x <= 230000:
        return '23'
    elif 230001 <= x <= 240000:
        return '24'
    elif 240001 <= x <= 250000:
        return '25'
    elif 250001 <= x <= 260000:
        return '26'
    elif 260001 <= x <= 270000:
        return '27'
    elif 270001 <= x <= 280000:
        return '28'
    elif 280001 <= x <= 290000:
        return '29'
    elif 290001 <= x <= 300000:
        return '30'


def userimagelocation(userid):
    if 1 <= userid <= 10000:
        return '1'
    elif 10001 <= userid <= 20000:
        return '2'
    elif 20001 <= userid <= 30000:
        return '3'
    elif 30001 <= userid <= 40000:
        return '4'
    elif 40001 <= userid <= 50000:
        return '5'
    elif 50001 <= userid <= 60000:
        return '6'
    elif 60001 <= userid <= 70000:
        return '7'
    elif 70001 <= userid <= 80000:
        return '8'
    elif 80001 <= userid <= 90000:
        return '9'
    elif 90001 <= userid <= 100000:
        return '10'
    elif 100001 <= userid <= 110000:
        return '11'
    elif 110001 <= userid <= 120000:
        return '12'
    elif 120001 <= userid <= 130000:
        return '13'
    elif 130001 <= userid <= 140000:
        return '14'
    elif 140001 <= userid <= 150000:
        return '15'
    elif 150001 <= userid <= 160000:
        return '16'
    elif 160001 <= userid <= 170000:
        return '17'
    elif 170001 <= userid <= 180000:
        return '18'
    elif 180001 <= userid <= 190000:
        return '19'
    elif 190001 <= userid <= 200000:
        return '20'
    elif 200001 <= userid <= 210000:
        return '21'
    elif 210001 <= userid <= 220000:
        return '22'
    elif 220001 <= userid <= 230000:
        return '23'
    elif 230001 <= userid <= 240000:
        return '24'
    elif 240001 <= userid <= 250000:
        return '25'
    elif 250001 <= userid <= 260000:
        return '26'
    elif 260001 <= userid <= 270000:
        return '27'
    elif 270001 <= userid <= 280000:
        return '28'
    elif 280001 <= userid <= 290000:
        return '29'
    elif 290001 <= userid <= 300000:
        return '30'


def floating_decimals(f_val, dec):
    prc = "{:."+str(dec)+"f}"  # first cast decimal as str
    return Decimal(prc.format(f_val))


def id_generator_picture1(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def id_generator_picture2(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def id_generator_picture3(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def id_generator_picture4(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def id_generator_picture5(size=30, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

#
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

#
# def usdtocurrency(price, currency):
#     getcurrentprice = db.session.query(btcPrices)\
#         .filter_by(currency_id=currency).first()
#     if currency == 1:
#         return price
#     else:
#         x = Decimal(price) / Decimal(getcurrentprice.price)
#         bt = (Decimal(getcurrentprice.price) * x)
#         c = '{0:.2f}'.format(bt)
#         return c
#
#
# def convertbtctolocal(amount, currency):
#     getcurrentprice = db.session.query(btcPrices) \
#         .filter_by(currency_id=currency).first()
#     bt = getcurrentprice.price
#     z = Decimal(bt) * Decimal(amount)
#     c = floating_decimals(z, 2)
#     return c

#
# def convertlocaltobtc(amount, currency):
#     getcurrentprice = db.session.query(btcPrices) \
#         .filter_by(currency_id=currency).first()
#
#     bt = getcurrentprice.price
#     z = Decimal(amount) / Decimal(bt)
#     c = floating_decimals(z, 8)
#     return c


def priceaftermargin_btccash(margin, currency):
    getcurrentprice = db.session.query(btc_cash_Prices) \
        .filter_by(currency_id=currency).first()
    marginq = db.session.query(Query_margin).filter_by(id=margin).first()
    margin1 = marginq.value

    bt = getcurrentprice.price
    z = margin1
    if 0 > margin1:
        newprice = (z * (-bt))
        x = (newprice - bt)
        y = (Decimal(bt) - Decimal(x))
        c = '{0:.2f}'.format(y)
        return c
    else:
        y = Decimal(z * bt)
        c = '{0:.2f}'.format(y)
        return c


def btc_cash_converttolocal(amount, currency):
    getcurrentprice = db.session.query(btc_cash_Prices) \
        .filter_by(currency_id=currency).first()

    bt = getcurrentprice.price
    z = Decimal(bt) * Decimal(amount)
    c = floating_decimals(z, 2)
    return c


def btc_cash_convertlocaltobtc(amount, currency):
    getcurrentprice = db.session.query(btc_cash_Prices) \
        .filter_by(currency_id=currency).first()

    bt = getcurrentprice.price
    z = Decimal(amount) / Decimal(bt)
    c = floating_decimals(z, 8)
    return c
