


def headerfunctions():
    from flask_login import current_user
    from app import db
    from app.classes.auth import User
    from app.classes.message import PostUser, Notifications
    from app.classes.item import ShoppingCart
    from app.classes.service import Issue
    from app.classes.vendor import Orders
    from app.classes.wallet_bch import BchWallet
    from sqlalchemy.sql import func, or_
    from decimal import Decimal
    if current_user.is_authenticated:
        user = db.session.query(User).filter_by(username=current_user.username).first()

        # shopping cart total
        tcart = db.session.query(func.sum(ShoppingCart.quantity_of_item))
        tcart = tcart.filter(ShoppingCart.customer_id == user.id, ShoppingCart.savedforlater == 0)
        totalincart = tcart.all()

        # Vendor
        # issues count
        # disputes orders as vendor
        rdispute = db.session.query(Orders)
        rdispute = rdispute.filter(Orders.completed == 0)
        rdispute = rdispute.filter(Orders.vendor_id == user.id)
        rdispute = rdispute.filter(or_(
                                   Orders.request_return != 0,
                                   Orders.disputed_order == 1))
        returndispute = rdispute.count()

        # Customer
        #  service issues count
        # GET customer issues
        # new orders for physical items
        norders = db.session.query(Orders.new_order)
        norders = norders.filter(Orders.vendor_id == user.id, Orders.new_order == 1)
        neworders = norders.count()

        # See if user has any active issues for the sidebar
        posts = db.session.query(Issue)
        posts = posts.filter(Issue.author_id == current_user.id)
        posts = posts.filter(Issue.status == 0)
        posts = posts.order_by(Issue.timestamp.desc())
        thepostcount = posts.count()

        # get returns or disputes as a customer
        myordersissues = db.session.query(Orders)
        myordersissues = myordersissues.filter(Orders.customer == current_user.username)
        myordersissues = myordersissues.filter(or_(Orders.disputed_order == 1, Orders.request_return == 2))
        myordersissues = myordersissues.order_by(Orders.age.desc())
        myordersissuesfullcount = myordersissues.count()


        # notifications
        gnotifications = db.session.query(Notifications.read)
        gnotifications = gnotifications.filter(Notifications.userid == user.id, Notifications.read == 1)
        genotifications = gnotifications.count()

        # Get New messages count
        newmsg = db.session.query(PostUser)
        newmsg = newmsg.filter(PostUser.userid == current_user.id)
        newmsg = newmsg.filter(PostUser.unread == 1)
        allmsgcount = newmsg.count()

        userwallet = db.session.query(BchWallet).filter_by(userid=user.id).first()

        try:
            userbalance = Decimal(userwallet.currentbalance)
            unconfirmed = Decimal(userwallet.unconfirmed)
        except:
            userbalance = 0
            unconfirmed = 0
        tot = (totalincart[0][0])
        if tot is None:
            tot = 0

    else:
        allmsgcount = 0

        neworders = 0
        returndispute = 0
        genotifications = 0
        thepostcount = 0
        user = 0
        tot = 0
        userbalance = 0
        unconfirmed = 0
        myordersissuesfullcount = 0

    # this is the total issues(returns, service, disputes)
    # customer issues
    customerdisputes = (int(thepostcount)) + (int(myordersissuesfullcount))
    # vendor
    #  issues
    issues = (int(returndispute))
    # new orders
    order = (int(neworders))

    # both
    getnotifications = (int(genotifications))
    return user, order, tot, issues, getnotifications, allmsgcount, userbalance, unconfirmed, customerdisputes

def headerfunctions_vendor():
    from flask_login import current_user
    from app import db
    from app.classes.auth import User
    from app.classes.message import Notifications
    from app.classes.vendor import Orders
    from sqlalchemy.sql import or_

    user = db.session.query(User).filter_by(username=current_user.username).first()

    # GET customer issues
    myorderscount = db.session\
    .query(Orders)\
    .filter(Orders.customer == current_user.username)\
    .filter(or_(Orders.disputed_order == 1, Orders.request_return == 2))\
    .count()

    # new orders for physical items
    neworders = db.session\
    .query(Orders.new_order)\
    .filter(Orders.vendor_id == user.id, Orders.new_order == 1)\
    .count()

    # disputes orders
    rdispute = db.session\
    .query(Orders)\
    .filter(Orders.completed == 0)\
    .filter(Orders.vendor_id == user.id)\
    .filter(or_(
    Orders.request_return != 0,
    Orders.disputed_order == 1))\
    .count()

    # notifications
    gnotifications = db.session\
    .query(Notifications.read)\
    .filter(Notifications.userid == user.id, Notifications.read == 1)\
    .count()

    issues = (int(rdispute))
    order = (int(neworders))
    getnotifications = (int(gnotifications))
    customerdisputes = int(myorderscount)

    return user, order,  issues, getnotifications, customerdisputes

