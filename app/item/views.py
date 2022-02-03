from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.item import item
from app import db
from decimal import Decimal
from datetime import datetime, timedelta
import calendar
from sqlalchemy.sql.expression import func
from app.item.forms import \
    additemForm, \
    shoppingcartForm, \
    checkoutForm, \
    custominfo, \
    custominfoDelete, \
    flagListing, \
    promoandgiftform

from app.search.forms import searchForm

# models
from app.classes.models import \
    btc_cash_Prices

from app.classes.auth import User, UserFees

from app.classes.achievements import \
    UserAchievements, whichAch

from app.classes.admin import \
    flagged

from app.classes.item import \
    marketItem, \
    ShoppingCart, \
    ShoppingCartTotal, \
    ItemtoDelete

from app.classes.profile import \
    StatisticsVendor

from app.classes.service import \
    shippingSecret

from app.classes.userdata import \
    Feedback

from app.classes.vendor import \
    Orders

from app.classes.wallet_bch import \
    BchWallet

from app.classes.affiliate import \
    AffiliateOverview, \
    AffiliateStats
# endmodels

from app.achievements.c import firstpurchase
from app.achievements.v import firstsale
from app.search.searchfunction import headerfunctions
from app.subq.related import relatedtoItem
from app.userdata.views import \
    differenttradingpartners_user, \
    differenttradingpartners_vendor, \
    vendorflag, \
    addflag

from app.notification import notification

from app.common.functions import \
    floating_decimals, \
    btc_cash_convertlocaltobtc

from app.wallet_bch.wallet_btccash_work import btc_cash_sendCointoEscrow

from app.common.decorators import \
    ping_user, \
    website_offline, \
    login_required

from app import UPLOADED_FILES_DEST


@item.route('/<int:id>', methods=['GET', 'POST'])
@website_offline
@ping_user
def Itemforsale(id):
    now = datetime.utcnow()
    preview = 0
    # forms
    formsearch = searchForm()
    formcart = additemForm(request.form)
    flag = flagListing()

    # header functions
    user, \
        order, \
        tot, \
        issues, \
        getnotifications, \
        allmsgcount, \
        userbalance, \
        unconfirmed, \
        customerdisputes = headerfunctions()

    # Get the item query
    try:
        vendoritem = marketItem.query.get(id)
        if vendoritem is None:
            flash("item is no longer available", category="primary")
            return redirect(url_for('index', username=current_user.username))
        else:
            vendoritem = vendoritem
            # add count to item viewed
            addviewer = int(vendoritem.viewcount) + 1
            vendoritem.viewcount = int(addviewer)
            db.session.add(vendoritem)
            db.session.flush()
    except Exception:
        flash("item is no longer available", category="primary")
        return redirect(url_for('index', username=current_user.username))

    # facebook twitter info
    itemurl = 'https://www.clearnetmarket.com/info/item/item/' \
              + str(vendoritem.stringnodeid) \
              + str(vendoritem.stringauctionid) \
              + str(vendoritem.imageone)
    converprice = btc_cash_convertlocaltobtc(
        amount=vendoritem.price, currency=vendoritem.currency)
    socialdescriptiontwitter = str('You Can buy this item for bitcoin on Clearnet Market for ') \
        + "\n\n" + str(converprice) + 'BTC'

    # get flagged status for current user
    finditem = db.session.query(flagged).filter_by(
        listingid=vendoritem.id).first()

    # vendor info
    vendor = db.session.query(User).filter_by(id=vendoritem.vendor_id).first()
    vendorstats = db.session.query(
        StatisticsVendor).filter_by(vendorid=vendor.id).first()
    vendorgetlevel = db.session.query(UserAchievements).filter_by(
        username=vendor.username).first()
    vendorpictureid = str(vendorgetlevel.level)

    # Item Feedback
    itemfeedback = db.session.query(Feedback).filter_by(
        item_id=id).order_by(Feedback.timestamp.desc()).limit(25)
    feedbackofitemcount = db.session.query(Feedback).filter_by(
        item_id=id).order_by(Feedback.timestamp.desc()).count()

    # Vendor Feedback
    vendorfeedback = db.session.query(Feedback).filter_by(
        vendorid=vendoritem.vendor_id).order_by(Feedback.timestamp.desc()).limit(25)
    vendorfeedbackcount = db.session.query(Feedback).filter_by(
        vendorid=vendoritem.vendor_id).count()
    vendorach = db.session.query(whichAch).filter_by(
        user_id=vendoritem.vendor_id).first()

    # Relatedqueries
    # gets other vendor items he has for sale
    otheritemsvendorsellsfull = db.session\
        .query(marketItem)\
        .filter(marketItem.online == 1)\
        .filter(marketItem.imageone != '')\
        .filter(marketItem.vendor_id == vendor.id)\
        .order_by(marketItem.totalsold.desc())
    otheritemsvendorsells = otheritemsvendorsellsfull.limit(6)
    otheritemsvendorhascount = otheritemsvendorsells.count()

    # get items with same keyword
    otheritemssamekeywordfull = db.session\
        .query(marketItem)\
        .filter(marketItem.online == 1)\
        .filter(marketItem.imageone != '')\
        .filter(marketItem.keywords.like('%' + vendoritem.keywords + '%'))
    samekeyword = otheritemssamekeywordfull.limit(6)
    samekeywordcount = otheritemssamekeywordfull.count()

    # get top selling items in category
    topsellingcatfull = db.session\
        .query(marketItem)\
        .filter(marketItem.online == 1)\
        .filter(marketItem.imageone != '')\
        .filter(marketItem.categoryid0 == vendoritem.categoryid0)\
        .order_by(func.rand())
    topsellingcat = topsellingcatfull.limit(6)
    topsellingcatcount = topsellingcatfull.count()
    # End related Queries

    # see what currency the user wants to sell in
    if vendoritem.digital_currency2 == 1:
        defaultselectedcurrency = 2
    else:
        defaultselectedcurrency = 3

    # If they add the item to cart or do a search
    if request.method == 'POST':
        if formsearch.search.data and formsearch.validate_on_submit():
            # cats
            categoryfull = formsearch.category.data
            cat = categoryfull.id

            # catch dynamic variables
            if formsearch.searchString.data == '' and cat == 0:
                return redirect(url_for('index'))

            if formsearch.searchString.data == '':
                formsearch.searchString.data = cat

            return redirect(url_for('search.searchMaster',
                                    searchterm=formsearch.searchString.data,
                                    function=cat,
                                    ))

        if formcart.addtocart1.data:
            if current_user.is_authenticated:
                if current_user.id == vendoritem.vendor_id:
                    flash("You cannot buy your own item", category="danger")
                    return redirect(url_for('item.Itemforsale', id=vendoritem.id))
                else:
                    vendoritem = db.session.query(
                        marketItem).filter_by(id=id).first()
                    if vendoritem.online == 1:
                        getcart = db.session.query(ShoppingCart)\
                            .filter(current_user.id == ShoppingCart.customer_id)\
                            .filter(ShoppingCart.savedforlater == 0)
                        generalcart = getcart.all()
                        cartamount = getcart.count()

                        in_cart_already = []
                        for f in generalcart:
                            in_cart_already.append(f)
                        if vendoritem.id in in_cart_already:
                            flash("Item is in your cart already",
                                  category="danger")
                            return redirect(url_for('item.Itemforsale', id=vendoritem.id))
                        if cartamount < 5:
                            item = ShoppingCart(
                                customer=current_user.username,
                                customer_id=current_user.id,
                                vendor=vendoritem.vendor_name,
                                vendor_id=vendoritem.vendor_id,
                                title_of_item=vendoritem.itemtitlee,
                                image_of_item=vendoritem.imageone,
                                price_of_item=vendoritem.price,
                                quantity_of_item=1,
                                currency=vendoritem.currency,
                                stringauctionid=vendoritem.stringauctionid,
                                stringnodeid=vendoritem.stringnodeid,
                                return_policy=vendoritem.itemrefundpolicy,
                                savedforlater=0,
                                item_id=vendoritem.id,
                                vendorsupply=1,
                                shippinginfo0=vendoritem.shippinginfo0,
                                shippingdayleast0=vendoritem.shippingdayleast0,
                                shippingdaymost0=vendoritem.shippingdaymost0,
                                shippinginfo2=vendoritem.shippinginfo2,
                                shippingprice2=vendoritem.shippingprice2,
                                shippingdayleast2=vendoritem.shippingdayleast2,
                                shippingdaymost2=vendoritem.shippingdaymost2,
                                shippinginfo3=vendoritem.shippinginfo3,
                                shippingprice3=vendoritem.shippingprice3,
                                shippingdayleast3=vendoritem.shippingdayleast3,
                                shippingdaymost3=vendoritem.shippingdaymost3,
                                shippingfree=vendoritem.shippingfree,
                                shippingtwo=vendoritem.shippingtwo,
                                shippingthree=vendoritem.shippingthree,
                                return_allowed=vendoritem.return_allowed,
                                digital_currency1=vendoritem.digital_currency1,
                                digital_currency2=vendoritem.digital_currency2,
                                digital_currency3=vendoritem.digital_currency3,
                                selected_currency=defaultselectedcurrency,
                                selected_shipping=0,
                                selected_shipping_description=0,
                                final_shipping_price=0,
                                final_price=0,
                            )
                            db.session.add(item)
                            db.session.commit()
                            flash("Item Added to Cart", category="success")
                            return redirect(url_for('item.Itemforsale', id=vendoritem.id))

                        else:
                            # cart full..save for later
                            item = ShoppingCart(
                                customer=current_user.username,
                                customer_id=current_user.id,
                                vendor=vendoritem.vendor_name,
                                vendor_id=vendoritem.vendor_id,
                                title_of_item=vendoritem.itemtitlee,
                                image_of_item=vendoritem.imageone,
                                price_of_item=vendoritem.price,
                                quantity_of_item=1,
                                currency=vendoritem.currency,
                                vendorsupply=1,
                                stringauctionid=vendoritem.stringauctionid,
                                stringnodeid=vendoritem.stringnodeid,
                                return_policy=vendoritem.itemrefundpolicy,
                                savedforlater=1,
                                item_id=vendoritem.id,
                                shippinginfo0=vendoritem.shippinginfo0,
                                shippingdayleast0=vendoritem.shippingdayleast0,
                                shippingdaymost0=vendoritem.shippingdaymost0,
                                shippinginfo2=vendoritem.shippinginfo2,
                                shippingprice2=vendoritem.shippingprice2,
                                shippingdayleast2=vendoritem.shippingdayleast2,
                                shippingdaymost2=vendoritem.shippingdaymost2,
                                shippinginfo3=vendoritem.shippinginfo3,
                                shippingprice3=vendoritem.shippingprice3,
                                shippingdayleast3=vendoritem.shippingdayleast3,
                                shippingdaymost3=vendoritem.shippingdaymost3,
                                shippingfree=vendoritem.shippingfree,
                                shippingtwo=vendoritem.shippingtwo,
                                shippingthree=vendoritem.shippingthree,
                                return_allowed=vendoritem.return_allowed,
                                digital_currency1=vendoritem.digital_currency1,
                                digital_currency2=vendoritem.digital_currency2,
                                digital_currency3=vendoritem.digital_currency3,
                                selected_currency=defaultselectedcurrency,
                                selected_shipping=0,
                                selected_shipping_description=0,
                                final_shipping_price=0,
                                final_price=0,
                            )
                            db.session.add(item)
                            db.session.commit()
                            flash("Item Saved for later. Cart full",
                                  category="success")
                            return redirect(url_for('item.Itemforsale', id=vendoritem.id))
            else:
                flash("You need to be logged in to do that", category="danger")
                return redirect(url_for('item.Itemforsale', id=vendoritem.id))
        elif flag.flagit.data:
            # if user/admin wants to flag an item
            if current_user.is_authenticated:
                if current_user.admin_role == 0:
                    flash("You cannot mark as flagged till level 2",
                          category="danger")
                    return redirect(url_for('item.Itemforsale', id=vendoritem.id))
                else:
                    # add stats to user/vendor
                    addflag(user_id=current_user.id)
                    vendorflag(user_id=vendoritem.vendor_id)

                    if finditem:
                        if current_user.admin_role >= 2:
                            flash("Item deleted", category="danger")
                            return redirect(url_for('admin.deleteItem', id=vendoritem.id))
                        else:
                            howmanyalready = finditem.howmany
                            if howmanyalready == 6:
                                flash("Item deleted", category="danger")
                                return redirect(url_for('admin.deleteItem', id=vendoritem.id))
                            else:

                                if finditem.user_id2 == 0:
                                    newhowmany = howmanyalready + 1
                                    finditem.howmany = newhowmany
                                    finditem.user_id2 = current_user.id
                                    db.session.add(finditem)
                                    db.session.commit()
                                    flash("Item flagged for review",
                                          category="danger")
                                    return redirect(url_for('item.Itemforsale', id=vendoritem.id))
                                elif finditem.user_id3 == 0:
                                    newhowmany = howmanyalready + 1
                                    finditem.howmany = newhowmany
                                    finditem.user_id3 = current_user.id
                                    db.session.add(finditem)
                                    db.session.commit()
                                    flash("Item flagged for review",
                                          category="danger")
                                    return redirect(url_for('item.Itemforsale', id=vendoritem.id))
                                elif finditem.user_id4 == 0:
                                    newhowmany = howmanyalready + 1
                                    finditem.howmany = newhowmany
                                    finditem.user_id4 = current_user.id
                                    db.session.add(finditem)
                                    db.session.commit()
                                    flash("Item flagged for review",
                                          category="danger")
                                    return redirect(url_for('item.Itemforsale', id=vendoritem.id))
                                elif finditem.user_id5 == 0:
                                    newhowmany = howmanyalready + 1
                                    finditem.howmany = newhowmany
                                    finditem.user_id5 = current_user.id
                                    db.session.add(finditem)
                                    db.session.commit()
                                    flash("Item flagged for review",
                                          category="danger")
                                    return redirect(url_for('item.Itemforsale', id=vendoritem.id))
                                else:
                                    return redirect(url_for('item.Itemforsale', id=vendoritem.id))
                    else:
                        newflagged = flagged(
                            user_id=vendoritem.vendor_id,
                            vendorname=vendoritem.vendor_name,
                            listingtitle=vendoritem.itemtitlee,
                            howmany=1,
                            typeitem=1,
                            listingid=vendoritem.id,
                            flaggeduser_id1=current_user.id,
                            flaggeduser_id2=0,
                            flaggeduser_id3=0,
                            flaggeduser_id4=0,
                            flaggeduser_id5=0,
                        )
                        db.session.add(newflagged)
                        db.session.commit()
                        flash("Item flagged for review", category="warning")
                        return redirect(url_for('item.Itemforsale', id=vendoritem.id))

            else:
                flash("You must be logged in", category="warning")
                return redirect(url_for('item.Itemforsale', id=vendoritem.id))
        elif flag.banit.data:
            # if an admin wants to delete an item and ban its amazon id
            if current_user.is_authenticated:
                if current_user.admin_role >= 5:
                    banthisitem = ItemtoDelete(
                        itemid=vendoritem.id
                    )
                    db.session.add(banthisitem)
                    db.session.commit()
                    flash("Deleting this item.  Added to db", category="warning")
                    return redirect(url_for('item.Itemforsale', id=vendoritem.id))
                else:
                    return redirect(url_for('item.Itemforsale', id=vendoritem.id))
            else:
                return redirect(url_for('item.Itemforsale', id=vendoritem.id))

        else:
            return redirect(url_for('item.Itemforsale', id=vendoritem.id))

    # end forum post
    return render_template('/item/Item.html',
                           # forms
                           formcart=formcart,
                           form=formsearch,
                           item=vendoritem,
                           flag=flag,
                           # header stuff
                           order=order,
                           tot=tot,
                           issues=issues,
                           getnotifications=getnotifications,
                           allmsgcount=allmsgcount,
                           userbalance=userbalance,
                           unconfirmed=unconfirmed,
                           user=user,
                           now=now,
                           customerdisputes=customerdisputes,
                           # page stuff
                           preview=preview,
                           UPLOADED_FILES_DEST=UPLOADED_FILES_DEST,
                           socialdescriptiontwitter=socialdescriptiontwitter,
                           itemurl=itemurl,
                           finditem=finditem,
                           itemfeedback=itemfeedback,
                           vendorfeedback=vendorfeedback,
                           feedbackofitemcount=feedbackofitemcount,
                           vendorfeedbackcount=vendorfeedbackcount,
                           vendorstats=vendorstats,
                           vendor=vendor,
                           vendorgetlevel=vendorgetlevel,
                           vendorpictureid=vendorpictureid,
                           vendorach=vendorach,
                           # relatedqueries
                           otheritemsvendorsells=otheritemsvendorsells,
                           otheritemsvendorhascount=otheritemsvendorhascount,
                           samekeyword=samekeyword,
                           samekeywordcount=samekeywordcount,
                           topsellingcat=topsellingcat,
                           topsellingcatcount=topsellingcatcount
                           )


@item.route('/deletepicture/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def deletecartitem(id):
    try:
        user = db.session.query(User).filter_by(
            username=current_user.username).first()
        try:
            item = ShoppingCart.query.get(id)
            if item.customer_id == user.id:
                db.session.delete(item)
                db.session.commit()
                return redirect(url_for('item.shoppingcart', username=current_user.username))
            else:
                return redirect(url_for('item.shoppingcart', username=current_user.username))
        except Exception:
            return redirect(url_for('item.shoppingcart', username=current_user.username))
    except:
        return redirect(url_for('index', username=current_user.username))


@item.route('/saveforlater/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def savecartitem(id):
    try:
        user = db.session.query(User).filter_by(
            username=current_user.username).first()
        try:
            item = ShoppingCart.query.get(id)
            if item.customer_id == user.id:
                item.savedforlater = 1
                db.session.add(item)
                db.session.commit()
                return redirect(url_for('item.shoppingcart', username=current_user.username))
            else:
                return redirect(url_for('item.shoppingcart', username=current_user.username))
        except Exception:
            return redirect(url_for('item.shoppingcart', username=current_user.username))
    except:
        return redirect(url_for('index', username=current_user.username))


@item.route('/movefornow/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def movecartitem(id):
    try:
        theitem = ShoppingCart.query.get(id)
        if theitem:
            if theitem.customer_id == current_user.id:
                getcart = db.session\
                    .query(ShoppingCart)\
                    .filter(current_user.id == ShoppingCart.customer_id)\
                    .filter(ShoppingCart.savedforlater == 0)
                cartamount = getcart.count()
                if int(cartamount) > 5:
                    theitem.savedforlater = 1
                    db.session.add(theitem)
                    db.session.commit()
                    flash("Cart is full", category="danger")
                    return redirect(url_for('item.shoppingcart', username=current_user.username))
                else:
                    theitem.savedforlater = 0
                    db.session.add(theitem)
                    db.session.commit()
                    flash("Items moved to cart", category="success")
                    return redirect(url_for('item.shoppingcart', username=current_user.username))
            else:
                flash("Invalid Cart", category="danger")
                return redirect(url_for('item.shoppingcart', username=current_user.username))
        else:
            flash("Item is not available.", category="success")
            return redirect(url_for('index', username=current_user.username))
    except Exception:
        flash("Cart Error", category="danger")
        return redirect(url_for('item.shoppingcart', username=current_user.username))


@item.route('/create-shipping/', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def createshipping(id):
    try:
        user = db.session\
            .query(User)\
            .filter_by(username=current_user.username)\
            .first()
        try:
            theitem = ShoppingCart.query.get(id)
            if item.customer_id == user.id:
                theitem.savedforlater = 1
                db.session.add(theitem)
                db.session.commit()
                return redirect(url_for('item.shoppingcart', username=current_user.username))
            else:
                return redirect(url_for('item.shoppingcart', username=current_user.username))
        except Exception:
            return redirect(url_for('item.shoppingcart', username=current_user.username))
    except:
        return redirect(url_for('index', username=current_user.username))


@item.route('/preview/<int:id>', methods=['GET', 'POST'])
@website_offline
@ping_user
@login_required
def previewItem(id):
    now = datetime.utcnow()
    preview = 1
    try:
        vendoritem = marketItem.query.get(id)
        if vendoritem is None:
            flash("item is no longer available", category="primary")
            return redirect(url_for('index', username=current_user.username))
        else:
            pass
    except Exception:
        flash("item is no longer available", category="primary")
        return redirect(url_for('index', username=current_user.username))

    finditem = db.session.query(flagged).filter_by(
        listingid=vendoritem.id).first()

    # forms
    formsearch = searchForm()

    formcart = additemForm(request.form)
    flag = flagListing()

    user, \
        order, \
        tot, \
        issues, \
        getnotifications, \
        allmsgcount, \
        userbalance, \
        unconfirmed, \
        customerdisputes = headerfunctions()

    user = db.session\
        .query(User)\
        .filter_by(username=current_user.username)\
        .first()

    try:
        # add count to item viewed
        addviewer = int(vendoritem.viewcount) + 1
        vendoritem.viewcount = int(addviewer)
        db.session.add(vendoritem)
        db.session.commit()
    except Exception as e:
        return redirect(url_for('index', username=current_user.username))

    # vendor info
    vendor = db.session\
        .query(User)\
        .filter_by(id=vendoritem.vendor_id)\
        .first()
    vendorstats = db.session.query(
        StatisticsVendor).filter_by(vendorid=vendor.id).first()
    vendorgetlevel = db.session.query(UserAchievements).filter_by(
        username=vendor.username).first()
    vendorpictureid = str(vendorgetlevel.level)

    # Item Feedback
    itemfeedback = db.session.query(Feedback).filter_by(
        item_id=id).order_by(Feedback.timestamp.desc()).limit(25)
    feedbackofitemcount = db.session.query(Feedback).filter_by(
        item_id=id).order_by(Feedback.timestamp.desc()).count()
    # Vendor Feedback
    vendorfeedback = db.session.query(Feedback).filter_by(
        vendorid=vendoritem.vendor_id).order_by(Feedback.timestamp.desc()).limit(25)
    vendorfeedbackcount = db.session.query(Feedback).filter_by(
        vendorid=vendoritem.vendor_id).count()
    vendorach = db.session.query(whichAch).filter_by(
        user_id=vendoritem.vendor_id).first()

    # Relatedqueries
    # gets queries of related subcategory..if not enough will do main category
    itemsinrelated = relatedtoItem(id=vendoritem.id)
    relatedcount = itemsinrelated.count()

    return render_template('/item/Item.html',
                           UPLOADED_FILES_DEST=UPLOADED_FILES_DEST,
                           formcart=formcart,
                           form=formsearch,
                           item=vendoritem,
                           finditem=finditem,
                           # header stuff
                           preview=preview,
                           order=order,
                           tot=tot,
                           issues=issues,
                           getnotifications=getnotifications,
                           allmsgcount=allmsgcount,
                           userbalance=userbalance,
                           unconfirmed=unconfirmed,
                           user=user,
                           now=now,
                           customerdisputes=customerdisputes,
                           itemsinrelated=itemsinrelated,
                           relatedcount=relatedcount,
                           itemfeedback=itemfeedback,
                           vendorfeedback=vendorfeedback,
                           feedbackofitemcount=feedbackofitemcount,
                           vendorfeedbackcount=vendorfeedbackcount,

                           vendorstats=vendorstats,
                           vendor=vendor,
                           vendorgetlevel=vendorgetlevel,
                           vendorpictureid=vendorpictureid,
                           vendorach=vendorach,
                           flag=flag
                           )


@item.route('/cart/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def buyitagain(id):
    try:
        # get the item
        vendoritem = db.session.query(marketItem).filter_by(id=id).first()

        # see what currency the user wants t sell in/
        if vendoritem.digital_currency2 == 1:
            defaultselectedcurrency = 2
        else:
            defaultselectedcurrency = 3

        if vendoritem is not None:
            if vendoritem.online == 1:
                if current_user.is_authenticated:
                    if current_user.id == vendoritem.vendor_id:
                        flash("You cannot buy your own item", category="danger")
                        return redirect(url_for('index', username=current_user.username))
                    else:

                        getcart = db.session.query(ShoppingCart)
                        getcart = getcart.filter(
                            current_user.id == ShoppingCart.customer_id)
                        generalcart = getcart.all()
                        getcart = getcart.filter(
                            ShoppingCart.savedforlater == 0)
                        cartamount = getcart.count()
                        already_in_cart = []
                        for f in generalcart:
                            already_in_cart.append(f.item_id)
                        if vendoritem.id in already_in_cart:
                            flash("Item is in your cart already",
                                  category="danger")
                            return redirect(url_for('index', username=current_user.username))
                        if cartamount < 5:
                            additem = ShoppingCart(
                                customer=current_user.username,
                                customer_id=current_user.id,
                                vendor=vendoritem.vendor_name,
                                vendor_id=vendoritem.vendor_id,
                                title_of_item=vendoritem.itemtitlee,
                                image_of_item=vendoritem.imageone,
                                price_of_item=vendoritem.price,
                                quantity_of_item=1,
                                currency=vendoritem.currency,
                                stringauctionid=vendoritem.stringauctionid,
                                stringnodeid=vendoritem.stringnodeid,
                                return_policy=vendoritem.itemrefundpolicy,
                                savedforlater=0,
                                item_id=vendoritem.id,
                                vendorsupply=1,
                                shippinginfo0=vendoritem.shippinginfo0,
                                shippingdayleast0=vendoritem.shippingdayleast0,
                                shippingdaymost0=vendoritem.shippingdaymost0,
                                shippinginfo2=vendoritem.shippinginfo2,
                                shippingprice2=vendoritem.shippingprice2,
                                shippingdayleast2=vendoritem.shippingdayleast2,
                                shippingdaymost2=vendoritem.shippingdaymost2,
                                shippinginfo3=vendoritem.shippinginfo3,
                                shippingprice3=vendoritem.shippingprice3,
                                shippingdayleast3=vendoritem.shippingdayleast3,
                                shippingdaymost3=vendoritem.shippingdaymost3,
                                shippingfree=vendoritem.shippingfree,
                                shippingtwo=vendoritem.shippingtwo,
                                shippingthree=vendoritem.shippingthree,
                                return_allowed=vendoritem.return_allowed,
                                digital_currency1=vendoritem.digital_currency1,
                                digital_currency2=vendoritem.digital_currency2,
                                digital_currency3=vendoritem.digital_currency3,
                                selected_currency=defaultselectedcurrency,
                                selected_shipping=0,
                                selected_shipping_description=0,
                                final_shipping_price=0,
                                final_price=0,

                            )

                            db.session.add(additem)
                            db.session.commit()
                            flash("Item Added to Cart", category="success")
                            return redirect(url_for('item.shoppingcart', username=current_user.username))

                        else:
                            # cart full..save for later
                            additem = ShoppingCart(
                                customer=current_user.username,
                                customer_id=current_user.id,
                                vendor=vendoritem.vendor_name,
                                vendor_id=vendoritem.vendor_id,
                                title_of_item=vendoritem.itemtitlee,
                                image_of_item=vendoritem.imageone,
                                price_of_item=vendoritem.price,
                                quantity_of_item=1,
                                currency=vendoritem.currency,
                                vendorsupply=1,
                                stringauctionid=vendoritem.stringauctionid,
                                stringnodeid=vendoritem.stringnodeid,
                                return_policy=vendoritem.itemrefundpolicy,
                                savedforlater=1,
                                item_id=vendoritem.id,
                                shippinginfo0=vendoritem.shippinginfo0,
                                shippingdayleast0=vendoritem.shippingdayleast0,
                                shippingdaymost0=vendoritem.shippingdaymost0,
                                shippinginfo2=vendoritem.shippinginfo2,
                                shippingprice2=vendoritem.shippingprice2,
                                shippingdayleast2=vendoritem.shippingdayleast2,
                                shippingdaymost2=vendoritem.shippingdaymost2,
                                shippinginfo3=vendoritem.shippinginfo3,
                                shippingprice3=vendoritem.shippingprice3,
                                shippingdayleast3=vendoritem.shippingdayleast3,
                                shippingdaymost3=vendoritem.shippingdaymost3,
                                shippingfree=vendoritem.shippingfree,
                                shippingtwo=vendoritem.shippingtwo,
                                shippingthree=vendoritem.shippingthree,
                                return_allowed=vendoritem.return_allowed,
                                digital_currency1=vendoritem.digital_currency1,
                                digital_currency2=vendoritem.digital_currency2,
                                digital_currency3=vendoritem.digital_currency3,
                                selected_currency=defaultselectedcurrency,
                                selected_shipping=0,
                                selected_shipping_description=0,
                                final_shipping_price=0,
                                final_price=0,
                            )
                            db.session.add(additem)
                            db.session.commit()
                flash("Item Added to Cart", category="success")
                return redirect(url_for('item.shoppingcart,', username=current_user.username))
            else:
                flash("Item is not available.", category="success")
                return redirect(url_for('index', username=current_user.username))
        else:
            flash("Item is not available.", category="success")
            return redirect(url_for('index', username=current_user.username))
    except Exception as e:
        return redirect(url_for('index', username=current_user.username))


@item.route('/cart', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def shoppingcart():
    now = datetime.utcnow()
    form = shoppingcartForm(request.form)

    # Total cart
    user = db.session\
        .query(User)\
        .filter_by(username=current_user.username)\
        .first()
    cart = db.session\
        .query(ShoppingCart)\
        .filter(ShoppingCart.customer == current_user.username,
                ShoppingCart.savedforlater == 0)\
        .all()
    gettotalcart = db.session\
        .query(ShoppingCartTotal)\
        .filter_by(customer=user.id)\
        .first()

    # see if orders previous..delete them
    user_orders = db.session\
        .query(Orders)\
        .filter(Orders.customer_id == user.id)\
        .filter(Orders.type == 1)\
        .filter(Orders.incart == 1)\
        .all()

    # see if msg
    msg = db.session\
        .query(shippingSecret)\
        .filter_by(user_id=user.id, orderid=0)\
        .first()
    if msg:
        db.session.delete(msg)

    for i in user_orders:
        db.session.delete(i)

    # Saved for later cart
    try:
        cartsaved = db.session\
            .query(ShoppingCart)\
            .filter(ShoppingCart.customer == user.username, ShoppingCart.savedforlater == 1)\
            .all()
    except Exception:
        cartsaved = 0
    # timer
    fiftenminutes = timedelta(minutes=15)
    fromnow = datetime.utcnow() + fiftenminutes

    # Bitcoin cash
    BTC_CASH_pricelist = []
    BTC_CASH_shipping_pricelist = []
    btc_cash_wallet = db.session\
        .query(BchWallet)\
        .filter_by(user_id=user.id)\
        .first()

    # First query item get latest price/info/etc
    for i in cart:
        # see if still exists
        try:
            getitem = db.session\
                .query(marketItem)\
                .filter(marketItem.id == i.item_id)\
                .first()
        except Exception as e:
            flash(i.title_of_item +
                  " is not available.It has been removed from your cart", category="success")
            db.session.delete(i)
            db.session.commit()
            return redirect(url_for('item.shoppingcart', username=current_user.username))

        # image
        try:
            i.stringauctionid = '/' + str(i.item_id) + '/'
        except Exception as e:
            flash(i.title_of_item +
                  " is not available.  It has been removed from your cart", category="success")
            db.session.delete(i)
            db.session.commit()
            return redirect(url_for('item.shoppingcart', username=current_user.username))
        try:
            i.image_of_item = getitem.imageone
        except Exception as e:
            i.image_of_item = '0'

        # price
        try:
            i.price_of_item = getitem.price
        except Exception:
            flash(i.title_of_item +
                  " is not available.  It has been removed from your cart", category="success")
            db.session.delete(i)
            db.session.commit()
            return redirect(url_for('item.shoppingcart', username=current_user.username))

        # supply
        try:
            i.vendorsupply = getitem.itemcount
            if i.vendorsupply <= 0:
                flash(i.title_of_item + " has been sold out.  It has been removed from your cart",
                      category="success")
                db.session.delete(i)
                db.session.commit()
                return redirect(url_for('item.shoppingcart', username=current_user.username))
        except Exception as e:
            flash(i.title_of_item +
                  " is not available.  It has been removed from your cart", category="success")
            db.session.delete(i)
            db.session.commit()
            return redirect(url_for('item.shoppingcart', username=current_user.username))

        # shipping
        try:
            if i.shippingfree == 0 and i.shippingtwo == 0 and i.shippingthree == 0:
                flash("Item#" + str(i.id) +
                      ": Doesnt have a shipping method", category="danger")
                db.session.delete(i)
                db.session.commit()
                return redirect(url_for('item.shoppingcart', username=current_user.username))
        except Exception:
            return redirect(url_for('index', username=current_user.username))

        # shipping1
        try:
            i.shippinginfo0 = getitem.shippinginfo0,
            i.shippingdayleast0 = getitem.shippingdayleast0,
            i.shippingdaymost0 = getitem.shippingdaymost0,

        except Exception:
            i.shippinginfo0 = '',
            i.shippingdayleast0 = '',
            i.shippingdaymost0 = '',

        # shipping2
        try:
            i.shippinginfo2 = getitem.shippinginfo2,
            i.shippingprice2 = getitem.shippingprice2,
            i.shippingdayleast2 = getitem.shippingdayleast2,
            i.shippingdaymost2 = getitem.shippingdaymost2,

        except Exception:
            i.shippinginfo2 = '',
            i.shippingprice2 = '',
            i.shippingdayleast2 = '',
            i.shippingdaymost2 = '',

        # shipping 3
        try:
            i.shippinginfo3 = getitem.shippinginfo3,
            i.shippingprice3 = getitem.shippingprice3,
            i.shippingdayleast3 = getitem.shippingdayleast3,
            i.shippingdaymost3 = getitem.shippingdaymost3,

        except Exception:
            i.shippinginfo3 = '',
            i.shippingprice3 = '',
            i.shippingdayleast3 = '',
            i.shippingdaymost3 = '',

        db.session.add(i)
        db.session.flush()

        # if bitcoin cash
        # selected currency 3 = btc cash

        # get price
        getcurrentprice = db.session\
            .query(btc_cash_Prices)\
            .filter(btc_cash_Prices.currency_id == i.currency)\
            .first()

        btc_cash_bt = getcurrentprice.price
        btc_cash_z = Decimal(i.price_of_item) / Decimal(btc_cash_bt)

        # combined price
        itemamount = (Decimal(i.quantity_of_item))
        itemandquant = (floating_decimals(itemamount * btc_cash_z, 8))
        i.final_price = itemandquant

        # Get shipping
        if i.selected_shipping == 1:
            btc_cash_shipprice2 = 0
            i.final_shipping_price = 0
            i.selected_shipping_description = str(getitem.shippinginfo0) \
                + ': ' + '(' + str(getitem.shippingdayleast0) \
                + ' days to ' + str(getitem.shippingdaymost0) \
                + ' days)'

        elif i.selected_shipping == 2:
            # PRICE
            # get shipping price local currency
            shipprice = Decimal(getitem.shippingprice2)

            # convert it to btc cash
            btc_cash_shiprice1 = Decimal(btc_cash_convertlocaltobtc(amount=shipprice,
                                                                    currency=getitem.currency))

            # get it formatted correctly
            btc_cash_shipprice2 = (floating_decimals(btc_cash_shiprice1, 8))

            # times the shipping price times quantity
            shippingtotal = Decimal(itemamount) * Decimal(btc_cash_shipprice2)

            # return shipping price
            btc_cash_shiprice = (floating_decimals(shippingtotal, 8))

            # SHIPPING
            i.selected_shipping_description = str(getitem.shippinginfo2) \
                + ': ' + '(' \
                + str(getitem.shippingdayleast2) \
                + ' days to ' \
                + str(getitem.shippingdaymost2) \
                + ' days)'

            i.final_shipping_price = btc_cash_shiprice

        elif i.selected_shipping == 3:
            # PRICE
            # get shipping price local currency
            shipprice = Decimal(getitem.shippingprice3)
            # convert it to btc cash
            btc_cash_shiprice1 = (btc_cash_convertlocaltobtc(amount=shipprice,
                                                             currency=getitem.currency))
            # get it formatted correctly
            btc_cash_shipprice2 = (floating_decimals(btc_cash_shiprice1, 8))
            # times the shipping price times quantity
            shippingtotal = Decimal(itemamount) * Decimal(btc_cash_shipprice2)
            # return shipping price
            btc_cash_shiprice = (floating_decimals(shippingtotal, 8))

            # SHIPPING
            # concat info for shipping information
            i.selected_shipping_description = str(getitem.shippinginfo2) \
                + ': ' \
                + '(' \
                + str(getitem.shippingdayleast3) \
                + ' days to ' \
                + str(getitem.shippingdaymost3) \
                + ' days)'

            i.final_shipping_price = btc_cash_shiprice

        else:
            # see what shipping is avaliable as first choice ..
            if i.shippingfree == 1:
                btc_cash_shipprice2 = 0
                i.selected_shipping_description = 0
            elif i.shippingtwo == 1:
                btc_cash_shipprice2 = btc_cash_convertlocaltobtc(
                    amount=i.shippingprice2, currency=i.currency)
                i.selected_shipping_description = i.shippinginfo2
            elif i.shippingtwo == 1:
                btc_cash_shipprice2 = btc_cash_convertlocaltobtc(
                    amount=i.shippingprice3, currency=i.currency)
                i.selected_shipping_description = i.shippinginfo3
            else:
                btc_cash_shipprice2 = 0
                i.selected_shipping_description = 0

        # add totals to list for adding to shopping cart total
        BTC_CASH_pricelist.append((btc_cash_z, i.quantity_of_item))
        BTC_CASH_shipping_pricelist.append(
            (btc_cash_shipprice2, i.quantity_of_item))

        # Add to shopping cart
        db.session.add(i)
        db.session.flush()
    ###
    # TOTALS for shopping cart total
    ###

    # BTC CASH
    # multiply items in list together
    xx = tuple(a * b for a, b in BTC_CASH_pricelist)
    # add to get total
    bb = ("{0:.8f}".format(sum(xx)))
    btc_cash_sum = sum(j for i, j in BTC_CASH_pricelist)

    gettotalcart.btc_cash_sumofitem = btc_cash_sum
    gettotalcart.btc_cash_price = bb

    # shipping loop
    dd = tuple(t*h for t, h in BTC_CASH_shipping_pricelist)
    # add to get total
    ee = ("{0:.8f}".format(sum(dd)))
    gettotalcart.shipping_btc_cashprice = ee
    # get total
    btc_cash_thetotal = Decimal(bb) + Decimal(ee)
    gettotalcart.total_btc_cash_price = btc_cash_thetotal
    # remove/set affiliate
    gettotalcart.percent_off_order = 0
    gettotalcart.btc_cash_off = 0
    gettotalcart.btc_off = 0

    db.session.add(gettotalcart)

    # Relatedqueries
    # gets queries of related subcategory..if not enough will do main category
    # related to first item only currently
    cart1 = db.session\
        .query(ShoppingCart)\
        .filter(ShoppingCart.customer_id == user.id, ShoppingCart.savedforlater == 0)\
        .first()
    if cart1 is not None:
        itemsinrelated = relatedtoItem(id=cart1.item_id)
        relatedcount = itemsinrelated.count()
        related1 = 1
    else:
        itemsinrelated = 0
        relatedcount = 0
        related1 = 0

    # get price
    getcurrentprice = db.session\
        .query(btc_cash_Prices) \
        .filter(btc_cash_Prices.currency_id == current_user.currency) \
        .first()

    db.session.commit()

    if request.method == "POST":
        try:
            if form.update.data:
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('item.shoppingcart', username=user.username))
                else:
                    for y in cart:
                        # get to see whats checked
                        try:
                            checkbox = request.form.getlist(
                                ('checkit-' + str(y.id)))
                            valueincheckbox = checkbox[0]
                        except Exception:
                            valueincheckbox = 0
                            pass
                        try:
                            quant = request.form.getlist(
                                ('quant-' + str(y.id)))
                            # find out quant of whats checked
                            newquant = quant[0]
                        except Exception:
                            newquant = y.quantity_of_item
                            pass
                        try:
                            getcurrency = request.form.getlist(
                                ('currency-' + str(y.id)))
                            # find out quant of whats checked
                            thecurrency = getcurrency[0]
                        except Exception:
                            thecurrency = 0
                            pass
                        try:
                            shipmethod = request.form.getlist(
                                ('shipit-' + str(y.id)))
                            # find out quant of whats checked
                            shipmethodchosen = shipmethod[0]
                        except Exception:
                            shipmethodchosen = 0
                            pass
                        # query that specific item in shopping cart then update it
                        if valueincheckbox == 0:
                            pass
                        else:
                            # check to see if they picked a shipping method
                            if int(y.id) == int(valueincheckbox):
                                # see if item exists and check its shipping
                                markett = db.session.query(marketItem) \
                                    .filter(y.item_id == marketItem.id).first()
                                if int(markett.itemcount) < int(newquant):
                                    flash("Vendor does not have that much",
                                          category="danger")
                                    return redirect(url_for('item.shoppingcart', username=user.username))
                                else:
                                    y.quantity_of_item = newquant
                                    y.selected_currency = thecurrency

                                    if 1 <= int(shipmethodchosen) <= 3:
                                        y.selected_shipping = shipmethodchosen
                                    else:
                                        flash(
                                            "Please select a shipping method.", category="danger")
                                        return redirect(url_for('item.shoppingcart', username=user.username))
                                    db.session.add(y)
                                    db.session.commit()
                    return redirect(url_for('item.shoppingcart', username=current_user.username))

            elif form.delete.data:
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('item.shoppingcart', username=user.username))
                else:
                    for itemtobedeleted in cart:
                        try:
                            # get ites checked
                            checkbox = request.form.getlist(
                                ('checkit-' + str(itemtobedeleted.id)))
                            valueincheckbox = checkbox[0]
                        except Exception:
                            valueincheckbox = 0
                            pass
                        if valueincheckbox == 0:
                            pass
                        else:
                            # match item checked to cart
                            cartitem = db.session.query(ShoppingCart).filter_by(
                                id=valueincheckbox).first()
                            # if owner
                            if cartitem.customer == current_user.username:
                                # delete it
                                db.session.delete(cartitem)
                                db.session.commit()
                    return redirect(url_for('item.shoppingcart', username=current_user.username))

            elif form.saveforlater.data:
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('item.shoppingcart', username=user.username))
                else:
                    for y in cart:
                        try:
                            checkbox = request.form.getlist(
                                ('checkit-' + str(y.id)))
                            valueincheckbox = checkbox[0]
                        except Exception:
                            valueincheckbox = 0
                            pass
                        if valueincheckbox == 0:
                            pass
                        else:
                            cartitem = db.session.query(ShoppingCart).filter_by(
                                id=valueincheckbox).first()
                            if cartitem.customer == current_user.username:
                                cartitem.savedforlater = 1

                                db.session.add(cartitem)
                                db.session.commit()
                    return redirect(url_for('item.shoppingcart', username=current_user.username))

            elif form.gotocheckout.data:
                if gettotalcart.btcprice == 0 and gettotalcart.total_btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('item.shoppingcart', username=user.username))
                else:
                    for k in cart:
                        if k.selected_currency == 3:
                            # get price
                            getcurrentprice = db.session.query(btc_cash_Prices) \
                                .filter(btc_cash_Prices.currency_id == k.currency).first()
                        elif k.selected_currency == 2:
                            # get price
                            getcurrentprice = db.session.query(btc_cash_Prices) \
                                .filter(btc_cash_Prices.currency_id == k.currency).first()
                        else:
                            pass
                        priceofeach = Decimal(
                            k.final_price) / Decimal(k.quantity_of_item)

                        # # get the vendor fee currently
                        # #get the vendor match to userfees
                        getvendor = k.vendor_id
                        sellerfee = db.session.query(UserFees).filter(
                            UserFees.user_id == getvendor).first()
                        physicalitemfee = sellerfee.vendorfee
                        dbfeetopercent = (floating_decimals(
                            (physicalitemfee/100), 8))
                        fee = (floating_decimals(
                            (dbfeetopercent * k.final_price), 8))
                        # addfee to main amount requested
                        order = Orders(
                            type=1,
                            vendor='',
                            vendor_id=0,
                            quantity=k.quantity_of_item,
                            title=k.title_of_item,
                            new_order=1,
                            accepted_order=0,
                            waiting_order=0,
                            delivered_order=0,
                            customer=current_user.username,
                            customer_id=current_user.id,
                            age=datetime.utcnow(),
                            returncancelage=datetime.utcnow(),
                            return_by=datetime.utcnow() + timedelta(days=14),
                            private_note='',
                            escrow=0,
                            disputed_order=0,
                            item_id=k.item_id,
                            stringauctionid=k.stringauctionid,
                            stringnodeid=k.stringnodeid,
                            imageone=k.image_of_item,
                            request_cancel=0,
                            reason_cancel=0,
                            overallreason=0,
                            request_return=0,
                            currency=k.currency,
                            return_id=0,
                            cancelled=0,
                            feedback=0,
                            userfeedback=0,
                            completed=0,
                            completed_time=now,
                            disputedtimer=datetime.utcnow(),
                            modid=0,
                            incart=1,
                            fee=fee,
                            shipdescription=k.selected_shipping_description,
                            return_allowed=k.return_allowed,
                            buyorsell=0,
                            released=0,
                            return_quantity=0,
                            return_amount=0,
                            digital_currency=k.selected_currency,
                            price=k.final_price,
                            price_peritem=priceofeach,
                            perbtc=getcurrentprice.price,
                            shipping_price=k.final_shipping_price,
                            price_beforediscount=0,
                            affiliate_discount_percent=0,
                            affiliate_code='0',
                            affiliate_discount_btc=0,
                            affiliate_discount_btc_cash=0,
                            affiliate_profit=0,
                        )
                        db.session.add(order)

                    user.shopping_timer = fromnow
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for('item.checkout', username=current_user.username))

            else:
                flash("Invalid form", category="danger")
                return redirect(url_for('item.shoppingcart', username=current_user.username))
        except Exception as e:
            db.session.rollback()
            flash("Invalid Forms", category="danger")
            return redirect(url_for('item.shoppingcart', username=current_user.username))
    return render_template('/item/shoppingcart.html',
                           cart=cart,
                           cartsaved=cartsaved,
                           gettotalcart=gettotalcart,
                           form=form,
                           btc_cash_wallet=btc_cash_wallet,
                           relatedcount=relatedcount,
                           itemsinrelated=itemsinrelated,
                           related1=related1
                           )


@item.route('/checkout', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def checkout():
    # forms
    secretinfo = custominfo()
    secretinfoDelete = custominfoDelete()
    finalize = checkoutForm()
    promogift = promoandgiftform()

    promocodesadded = []
    # get user and car
    user = db.session\
        .query(User)\
        .filter_by(username=current_user.username)\
        .first()

    gettotalcart = db.session\
        .query(ShoppingCartTotal)\
        .filter_by(customer=user.id)\
        .first()

    # turn back if issue
    if gettotalcart.btc_sumofitem == 0 and gettotalcart.btc_cash_sumofitem == 0:
        flash("No Items in your Shopping Cart.", category="danger")
        return redirect(url_for('item.shoppingcart', username=user.username))
    if datetime.utcnow() >= user.shopping_timer:
        flash("Time ran out.  Please try again.", category="danger")
        return redirect(url_for('item.shoppingcart', username=user.username))

    # see if user has the Coin
    btc_cash_wallet = db.session\
        .query(BchWallet)\
        .filter_by(user_id=user.id)\
        .first()
    gettotalcart = db.session\
        .query(ShoppingCartTotal)\
        .filter_by(customer=user.id)\
        .first()

    # if user doesnt have enough money
    if Decimal(btc_cash_wallet.currentbalance) <= Decimal(gettotalcart.totalbtcprice):
        flash("Not enough coin in wallet ...", category="danger")
        return redirect(url_for('index'))

    # queries
    cart = db.session\
        .query(ShoppingCart)\
        .filter(ShoppingCart.customer == current_user.username, ShoppingCart.savedforlater == 0)\
        .all()

    # get the orders
    orders = db.session\
        .query(Orders)\
        .filter(Orders.customer_id == user.id)\
        .filter(Orders.type == 1).filter(Orders.incart == 1)\
        .group_by(Orders.id.asc())\
        .all()

    # see if promo code was added
    for promo in orders:
        if promo.affiliate_code != '0':
            promocodesadded.append(promo.affiliate_code)
    if len(promocodesadded) == 0:
        promocodewasadded = 0
    else:
        promocodewasadded = 1

    # get the message
    msg = db.session.query(shippingSecret).filter_by(
        user_id=user.id, orderid=0).first()
    if msg:
        secretmsg = 0
    else:
        secretmsg = 1

    # timer
    userstimeincart = user.shopping_timer
    timestamp = calendar.timegm(userstimeincart.utctimetuple()) * 1000

    if request.method == "POST":
        if current_user.id == gettotalcart.customer:
            # security to see if cart is empty
            if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                flash("No Items in your Shopping Cart.", category="danger")
                return redirect(url_for('item.shoppingcart'))
            if datetime.utcnow() >= user.shopping_timer:
                flash("Time ran out.  Please try again", category="danger")
                return redirect(url_for('item.shoppingcart'))

            # user added an address
            if secretinfo.custommsgbtn.data:
                # check to see if time ran out
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('item.shoppingcart'))
                elif datetime.utcnow() >= user.shopping_timer:
                    flash("Time ran out.  Please try again", category="danger")
                    return redirect(url_for('item.shoppingcart'))
                else:
                    if secretinfo.validate_on_submit():
                        try:
                            z = secretinfo.privatemsg.data
                            addmsg = shippingSecret(
                                user_id=current_user.id,
                                txtmsg=str(z),
                                timestamp=datetime.utcnow(),
                                orderid=0
                            )
                            db.session.add(addmsg)
                            db.session.commit()
                            return redirect(url_for('item.checkout'))
                        except Exception:
                            db.session.rollback()
                            return redirect(url_for('item.shoppingcart'))
                    else:
                        flash("Private Message form error. "
                              "10-2500 characters long required. No special characters allowed.",
                              category="danger")
                        return redirect(url_for('item.checkout'))

            # user deleted his message
            elif secretinfoDelete.deletemsgbtn.data:
                # check to see if cart items
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('item.shoppingcart'))
                # check to see if timer ran out
                elif datetime.utcnow() >= user.shopping_timer:
                    flash("Time ran out.  Please try again", category="danger")
                    return redirect(url_for('item.shoppingcart'))
                else:
                    db.session.delete(msg)
                    db.session.commit()
                    flash("Private Message deleted", category="danger")
                    return redirect(url_for('item.checkout'))

            # user added a promo or gift code
            elif promogift.addpromo.data:
                # check to see if cart items
                if promogift.validate_on_submit():
                    enteredcode = promogift.promocode.data

                    thepromo = db.session \
                        .query(AffiliateOverview) \
                        .filter(AffiliateOverview.promocode == enteredcode) \
                        .first()
                    if thepromo is not None:
                        thepromostats = db.session\
                            .query(AffiliateStats)\
                            .filter(AffiliateStats.user_id == thepromo.user_id)\
                            .first()
                        if thepromo.user_id != current_user.id:
                            if thepromostats is not None:
                                # new lists for the prices
                                newtotalforshopping_btc = []
                                newtotalforshopping_btc_cash = []
                                newtotalforshopping_btc_shipping = []
                                newtotalforshopping_btc_cash_shipping = []

                                for itemordered in orders:
                                    if itemordered.affiliate_code == '0':
                                        itemordered.affiliate_code = enteredcode
                                        itemordered.affiliate_discount_percent = thepromo.buyerdiscount
                                        itemordered.price_beforediscount = itemordered.price

                                        # percent off added to total
                                        gettotalcart.percent_off_order = thepromo.buyerdiscount
                                        # if item ordered was bitcoin

                                        # add entered orders to affiliate stats
                                        newwaitingpromo = thepromostats.promoenteredcount + 1
                                        thepromostats.promoenteredcount = newwaitingpromo
                                        db.session.add(thepromostats)

                                        if itemordered.digital_currency == 2:
                                            # change order
                                            itemordered.affiliate_discount_btc_cash = 0
                                            # price of order
                                            totalorderprice = Decimal(
                                                itemordered.price)
                                            # percent off
                                            thepromodiscountamount = (
                                                Decimal(thepromo.buyerdiscount) / 100)
                                            # amount saved
                                            amountsavings = (
                                                totalorderprice * thepromodiscountamount)
                                            itemordered.affiliate_discount_btc = amountsavings
                                            # adjust price per order and take off the money
                                            newpriceoforder = totalorderprice - amountsavings
                                            itemordered.price = newpriceoforder
                                            # change total
                                            # show percent off in total cart(add the balance up)
                                            addtooff = gettotalcart.btc_off + amountsavings
                                            gettotalcart.btc_off = addtooff

                                            db.session.add(gettotalcart)
                                            db.session.add(itemordered)

                                            # add new items to list
                                            newtotalforshopping_btc.append(
                                                (newpriceoforder, itemordered.quantity))
                                            newtotalforshopping_btc_shipping.append(
                                                (itemordered.shipping_price, itemordered.quantity))

                                            db.session.flush()
                                        # if item ordered was bitcoin cash
                                        else:
                                            # change order
                                            itemordered.affiliate_discount_btc = 0

                                            # price of order
                                            totalorderprice = Decimal(
                                                itemordered.price)

                                            # percent off
                                            thepromodiscountamount = (
                                                Decimal(thepromo.buyerdiscount) / 100)

                                            # amount saved
                                            amountsavings = (
                                                totalorderprice * thepromodiscountamount)
                                            itemordered.affiliate_discount_btc_cash = amountsavings

                                            # adjust price per order and take off the money
                                            newpriceoforder = totalorderprice - amountsavings
                                            itemordered.price = newpriceoforder
                                            # change total
                                            # show percent off in total cart
                                            addtooff = gettotalcart.btc_cash_off + amountsavings
                                            gettotalcart.btc_cash_off = addtooff

                                            db.session.add(gettotalcart)
                                            db.session.add(itemordered)

                                            # add new items to list
                                            newtotalforshopping_btc_cash.append(
                                                (newpriceoforder, itemordered.quantity))
                                            newtotalforshopping_btc_cash_shipping.append(
                                                (itemordered.shipping_price, itemordered.quantity))

                                            db.session.flush()
                                    else:
                                        flash(
                                            "Promo Code was already added...", category="danger")
                                        return redirect(url_for('item.checkout'))

                                # BTC CASH
                                # multiply items in list together
                                xx = tuple(
                                    a * b for a, b in newtotalforshopping_btc_cash)
                                # add to get total
                                bb = ("{0:.8f}".format(sum(xx)))
                                btc_cash_sum = sum(
                                    j for i, j in newtotalforshopping_btc_cash)

                                gettotalcart.btc_cash_sumofitem = btc_cash_sum
                                gettotalcart.btc_cash_price = bb

                                # shipping loop
                                dd = tuple(
                                    t * h for t, h in newtotalforshopping_btc_cash_shipping)
                                # add to get total
                                ee = ("{0:.8f}".format(sum(dd)))
                                gettotalcart.shipping_btc_cashprice = ee
                                # get total
                                btc_cash_thetotal = Decimal(bb) + Decimal(ee)
                                gettotalcart.total_btc_cash_price = btc_cash_thetotal

                                # commit changes to cart total
                                db.session.add(gettotalcart)
                                db.session.commit()

                                flash("Promo Code Added", category="success")
                                return redirect(url_for('item.checkout'))
                            else:
                                flash("Incorrect Promo Code",
                                      category="danger")
                                return redirect(url_for('item.checkout'))
                        else:
                            flash("Cannot use own promo code",
                                  category="danger")
                            return redirect(url_for('item.checkout'))
                    else:
                        flash("Promo Code Doesnt Exist..", category="danger")
                        return redirect(url_for('item.checkout'))

            # user confirmed payment
            elif finalize.MakePayment.data:

                # check to see if cart isnt empty
                if gettotalcart.btcprice == 0 and gettotalcart.btc_cash_price == 0:
                    flash("No Items in your Shopping Cart.", category="danger")
                    return redirect(url_for('item.shoppingcart'))
                # check to see if time still
                elif datetime.utcnow() >= user.shopping_timer:
                    flash("Time ran out.  Please try again", category="danger")
                    return redirect(url_for('item.shoppingcart'))
                else:
                    # add security here before proceeding
                    userwallet_btc_cash = db.session\
                        .query(BchWallet)\
                        .filter_by(user_id=user.id)\
                        .first()

                    thecurrentcarttotal_btc_cash = Decimal(
                        gettotalcart.total_btc_cash_price)

                    if thecurrentcarttotal_btc_cash > 0:
                        if Decimal(userwallet_btc_cash.currentbalance) <= thecurrentcarttotal_btc_cash:
                            flash("Not enough coin in bitcoin cash wallet",
                                  category="danger")
                            return redirect(url_for('wallet_btc.walletReceive', username=current_user.username))

                    # see if message
                    if (len(msg.txtmsg)) < 5:
                        flash("Message not long enough", category="danger")
                        return redirect(url_for('item.checkout'))
                    # customer has the coin..proceed
                    # loop through ORDERS..sendinc coin and doing transactions 1 by 1
                    # this doesnt loop through the shopping cart
                    for specificitemincart in order:
                        # get the item
                        # get specific item being purchased
                        try:
                            getitem = db.session\
                                .query(marketItem) \
                                .filter_by(id=specificitemincart.item_id) \
                                .first()
                        except Exception:
                            db.session.delete(specificitemincart)
                            db.session.commit()
                            flash(
                                "Could Not find Item. Perhaps the vendor removed it.", category="danger")
                            return redirect(url_for('wallet_btc.walletReceive', username=current_user.username))

                        # update the order to notify vendor
                        specificitemincart.incart = 0
                        specificitemincart.vendor = getitem.vendor_name,
                        specificitemincart.vendor_id = getitem.vendor_id,
                        # k.shipto_secretmsg = msg.txtmsg

                        # add total sold to item
                        newsold = int(getitem.totalsold) + \
                            int(specificitemincart.quantity)
                        newquantleft = int(getitem.itemcount) - \
                            int(specificitemincart.quantity)
                        getitem.totalsold = newsold
                        getitem.itemcount = newquantleft

                        # add diff trading partners
                        differenttradingpartners_user(user_id=specificitemincart.customer_id,
                                                      otherid=specificitemincart.vendor_id)

                        # add diff trading partners
                        differenttradingpartners_vendor(user_id=specificitemincart.vendor_id,
                                                        otherid=specificitemincart.customer_id)

                        # notify vendor
                        notification(type=1,
                                     username=specificitemincart.vendor,
                                     user_id=specificitemincart.vendor_id,
                                     salenumber=specificitemincart.id,
                                     bitcoin=0)

                        notification(type=112,
                                     username=specificitemincart.customer,
                                     user_id=specificitemincart.customer_id,
                                     salenumber=specificitemincart.id,
                                     bitcoin=0)

                        # for each time..do a coin move
                        # get price of shipping+item * quantity
                        priceofitemorder = floating_decimals((specificitemincart.price
                                                              + specificitemincart.shipping_price), 8)

                        # transactions are added in the sendcoin functions
                        # subtraction of balances occur there also
                        # send bitcoin

                        btc_cash_sendCointoEscrow(
                            amount=priceofitemorder,
                            comment=specificitemincart.id,
                            user_id=specificitemincart.customer_id
                        )

                        # achievement for first purchase
                        # in a loop since could be ten items
                        firstsale(user_id=specificitemincart.vendor_id)

                        # add a message for each order
                        addmsg = shippingSecret(
                            user_id=current_user.id,
                            txtmsg=msg.txtmsg,
                            timestamp=datetime.utcnow(),
                            orderid=specificitemincart.id
                        )

                        db.session.add(specificitemincart)
                        db.session.add(getitem)
                        db.session.add(addmsg)
                        db.session.flush()

                        # turn off if item is less than one
                        if getitem.itemcount < 1:

                            getitem.online = 0
                            db.session.add(getitem)

                            # send notification to vendor saying its all sold out
                            notification(type=9,
                                         username=specificitemincart.vendor,
                                         user_id=getitem.vendor_id,
                                         salenumber=getitem.id,
                                         bitcoin=0)

                # FINISHED loop
                # delete and clear everything
                # query for users message
                oldmsg = db.session\
                    .query(shippingSecret)\
                    .filter_by(user_id=user.id, orderid=0)\
                    .first()
                db.session.delete(oldmsg)

                # clear user shoppingcarttotal
                gettotalcart = db.session \
                    .query(ShoppingCartTotal) \
                    .filter_by(customer=user.id) \
                    .first()
                gettotalcart.totalbtcprice = 0
                gettotalcart.btcprice = 0
                gettotalcart.shippingbtcprice = 0

                # remove affiliate code
                gettotalcart.percent_off_order = 0
                gettotalcart.btc_cash_off = 0
                gettotalcart.btc_off = 0
                db.session.add(gettotalcart)

                # delete items in cart
                for f in cart:
                    db.session.delete(f)

                # achievement
                firstpurchase(user_id=current_user.id)

                db.session.commit()
                flash("Successful Order.", category="success")
                return redirect(url_for('auth.orders'))

        # not specific form information made
        else:
            flash("Form Error", category="danger")
            return redirect(url_for('item.checkout', username=user.username))

    return render_template('/item/checkout.html',
                           promogift=promogift,
                           secretinfo=secretinfo,
                           secretinfoDelete=secretinfoDelete,
                           finalize=finalize,
                           secretmsg=secretmsg,
                           msg=msg,
                           order=order,
                           cart=cart,
                           btc_cash_wallet=btc_cash_wallet,
                           timestamp=timestamp,
                           gettotalcart=gettotalcart,
                           promocodewasadded=promocodewasadded
                           )
