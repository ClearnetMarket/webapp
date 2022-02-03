from app import db
from app.classes.wallet_bch import \
    BchWallet
from decimal import \
    Decimal


def checkbalance_btccash(user_id, amount):
    # The money requested during the trade
    userwallet = db.session\
        .query(BchWallet)\
        .filter_by(user_id=user_id)\
        .first()
    theusersbalance = userwallet.currentbalance
    theamountrequested = Decimal(amount)

    if theusersbalance >= theamountrequested:
        return 1
    else:
        return 0
