

def headerfunctions():
    from flask_login import current_user
    from app import db
    from app.classes.auth import Auth_User
    from app.classes.message import Message_PostUser, Message_Notifications
    from app.classes.item import Item_CheckoutShoppingCart
    from app.classes.service import Service_Issue
    from app.classes.vendor import Vendor_Orders
    from app.classes.wallet_bch import Bch_Wallet
    from sqlalchemy.sql import func, or_
    from decimal import Decimal
    
    
    if current_user.is_authenticated:
        user = db.session.query(Auth_User).filter_by(
            username=current_user.username).first()

        # shopping cart total
        tcart = db.session.query(
            func.sum(Item_CheckoutShoppingCart.quantity_of_item))
        tcart = tcart.filter(Item_CheckoutShoppingCart.customer_id ==
                             user.id, Item_CheckoutShoppingCart.savedforlater == 0)
        totalincart = tcart.all()

        # Vendor
        # issues count
        # disputes orders as vendor
        rdispute = db.session.query(Vendor_Orders)
        rdispute = rdispute.filter(Vendor_Orders.completed == 0)
        rdispute = rdispute.filter(Vendor_Orders.vendor_id == user.id)
        rdispute = rdispute.filter(or_(
                                   Vendor_Orders.request_return != 0,
                                   Vendor_Orders.disputed_order == 1))
        returndispute = rdispute.count()

        # Customer
        #  service issues count
        # GET customer issues
        # new orders for physical items
        norders = db.session.query(Vendor_Orders.new_order)
        norders = norders.filter(
            Vendor_Orders.vendor_id == user.id, Vendor_Orders.new_order == 1)
        neworders = norders.count()

        # See if user has any active issues for the sidebar
        posts = db.session.query(Service_Issue)
        posts = posts.filter(Service_Issue.author_id == current_user.id)
        posts = posts.filter(Service_Issue.status == 0)
        posts = posts.order_by(Service_Issue.timestamp.desc())
        thepostcount = posts.count()

        # get returns or disputes as a customer
        myordersissues = db.session.query(Vendor_Orders)
        myordersissues = myordersissues.filter(
            Vendor_Orders.customer == current_user.username)
        myordersissues = myordersissues.filter(
            or_(Vendor_Orders.disputed_order == 1, Vendor_Orders.request_return == 2))
        myordersissues = myordersissues.order_by(Vendor_Orders.age.desc())
        myordersissuesfullcount = myordersissues.count()

        # notifications
        gnotifications = db.session.query(Message_Notifications.read)
        gnotifications = gnotifications.filter(
            Message_Notifications.user_id == user.id, Message_Notifications.read == 1)
        genotifications = gnotifications.count()

        # Get New messages count
        newmsg = db.session.query(Message_PostUser)
        newmsg = newmsg.filter(Message_PostUser.user_id == current_user.id)
        newmsg = newmsg.filter(Message_PostUser.unread == 1)
        allmsgcount = newmsg.count()

        userwallet = db.session.query(
            Bch_Wallet).filter_by(user_id=user.id).first()

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
    from app.classes.auth import Auth_User
    from app.classes.message import Message_Notifications
    from app.classes.vendor import Vendor_Orders
    from sqlalchemy.sql import or_

    user = db.session.query(Auth_User).filter_by(
        username=current_user.username).first()

    # GET customer issues
    myorderscount = db.session\
        .query(Vendor_Orders)\
        .filter(Vendor_Orders.customer == current_user.username)\
        .filter(or_(Vendor_Orders.disputed_order == 1, Vendor_Orders.request_return == 2))\
        .count()

    # new orders for physical items
    neworders = db.session\
        .query(Vendor_Orders.new_order)\
        .filter(Vendor_Orders.vendor_id == user.id, Vendor_Orders.new_order == 1)\
        .count()

    # disputes orders
    rdispute = db.session\
        .query(Vendor_Orders)\
        .filter(Vendor_Orders.completed == 0)\
        .filter(Vendor_Orders.vendor_id == user.id)\
        .filter(or_(
            Vendor_Orders.request_return != 0,
            Vendor_Orders.disputed_order == 1))\
        .count()

    # notifications
    gnotifications = db.session\
        .query(Message_Notifications.read)\
        .filter(Message_Notifications.user_id == user.id, Message_Notifications.read == 1)\
        .count()

    issues = (int(rdispute))
    order = (int(neworders))
    getnotifications = (int(gnotifications))
    customerdisputes = int(myorderscount)

    return user, order,  issues, getnotifications, customerdisputes
