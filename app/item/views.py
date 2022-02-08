from flask import \
    render_template, \
    redirect, \
    url_for, \
    flash, \
    request
from flask_login import current_user
from app.item import item
from app import db
from datetime import datetime
from sqlalchemy.sql.expression import func
from app.item.forms import \
    additemForm, \
    flagListing
from app.search.forms import searchForm

# models
from app.classes.auth import \
    User
from app.classes.achievements import \
    UserAchievements, \
    whichAch
from app.classes.admin import \
    flagged
from app.classes.item import \
    marketItem, \
    ShoppingCart, \
    ItemtoDelete
from app.classes.profile import \
    StatisticsVendor
from app.classes.userdata import \
    Feedback
# endmodels

from app.search.searchfunction import headerfunctions
from app.subq.related import relatedtoItem
from app.userdata.views import \
    vendorflag, \
    addflag
from app.common.functions import \
    btc_cash_convertlocaltobtc
from app.common.decorators import \
    ping_user, \
    website_offline, \
    login_required
from app import UPLOADED_FILES_DEST


@item.route('/<int:id>', methods=['GET', 'POST'])
@website_offline
@ping_user
def itemforsale(id):
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
    finditem = db.session\
        .query(flagged)\
        .filter_by(listingid=vendoritem.id)\
        .first()

    # vendor info
    vendor = db.session\
        .query(User)\
        .filter_by(id=vendoritem.vendor_id)\
        .first()
    vendorstats = db.session\
        .query(StatisticsVendor)\
        .filter_by(vendorid=vendor.id)\
        .first()
    vendorgetlevel = db.session\
        .query(UserAchievements)\
        .filter_by(username=vendor.username)\
        .first()
    vendorpictureid = str(vendorgetlevel.level)

    # Item Feedback
    itemfeedback = db.session\
        .query(Feedback)\
        .filter_by(item_id=id)\
        .order_by(Feedback.timestamp.desc())\
        .limit(25)
    feedbackofitemcount = db.session\
        .query(Feedback)\
        .filter_by(item_id=id)\
        .order_by(Feedback.timestamp.desc())\
        .count()

    # Vendor Feedback
    vendorfeedback = db.session\
        .query(Feedback)\
        .filter_by(vendorid=vendoritem.vendor_id)\
        .order_by(Feedback.timestamp.desc())\
        .limit(25)

    vendorfeedbackcount = db.session\
        .query(Feedback)\
        .filter_by(vendorid=vendoritem.vendor_id)\
        .count()

    vendorach = db.session.query(whichAch).filter_by(
        user_id=vendoritem.vendor_id).first()

    # Related queries
    # gets other vendor items he has for sale
    otheritemsvendorsellsfull = db.session\
        .query(marketItem)\
        .filter(marketItem.online == 1)\
        .filter(marketItem.imageone != '0')\
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
        .order_by(func.random())
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
        if formsearch.validate_on_submit():
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
                    return redirect(url_for('item.itemforsale', id=vendoritem.id))
                else:
                    vendoritem = db.session\
                        .query(marketItem)\
                        .filter_by(id=id)\
                        .first()
                    if vendoritem.online == 1:
                        getcart = db.session\
                            .query(ShoppingCart)\
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
                            return redirect(url_for('item.itemforsale', id=vendoritem.id))
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
                            return redirect(url_for('item.itemforsale', id=vendoritem.id))
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
                            return redirect(url_for('item.itemforsale', id=vendoritem.id))
            else:
                flash("You need to be logged in to do that", category="danger")
                return redirect(url_for('item.itemforsale', id=vendoritem.id))
        elif flag.flagit.data:
            # if user/admin wants to flag an item
            if current_user.is_authenticated:
                if current_user.admin_role == 0:
                    flash("You cannot mark as flagged till level 2",
                          category="danger")
                    return redirect(url_for('item.itemforsale', id=vendoritem.id))
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
                                    return redirect(url_for('item.itemforsale', id=vendoritem.id))
                                elif finditem.user_id3 == 0:
                                    newhowmany = howmanyalready + 1
                                    finditem.howmany = newhowmany
                                    finditem.user_id3 = current_user.id
                                    db.session.add(finditem)
                                    db.session.commit()
                                    flash("Item flagged for review",
                                          category="danger")
                                    return redirect(url_for('item.itemforsale', id=vendoritem.id))
                                elif finditem.user_id4 == 0:
                                    newhowmany = howmanyalready + 1
                                    finditem.howmany = newhowmany
                                    finditem.user_id4 = current_user.id
                                    db.session.add(finditem)
                                    db.session.commit()
                                    flash("Item flagged for review",
                                          category="danger")
                                    return redirect(url_for('item.itemforsale', id=vendoritem.id))
                                elif finditem.user_id5 == 0:
                                    newhowmany = howmanyalready + 1
                                    finditem.howmany = newhowmany
                                    finditem.user_id5 = current_user.id
                                    db.session.add(finditem)
                                    db.session.commit()
                                    flash("Item flagged for review",
                                          category="danger")
                                    return redirect(url_for('item.itemforsale', id=vendoritem.id))
                                else:
                                    return redirect(url_for('item.itemforsale', id=vendoritem.id))
                    else:
                        newflagged = flagged(
                            user_id=vendoritem.vendor_id,
                            vendorname=vendoritem.vendor_name,
                            listingtitle=vendoritem.itemtitlee,
                            howmany=1,
                            typeitem=1,
                            listingid=vendoritem.id,
                            flagged_user_id_1=current_user.id,
                            flagged_user_id_2=0,
                            flagged_user_id_3=0,
                            flagged_user_id_4=0,
                            flagged_user_id_5=0,
                        )
                        db.session.add(newflagged)
                        db.session.commit()
                        flash("Item flagged for review", category="warning")
                        return redirect(url_for('item.itemforsale', id=vendoritem.id))

            else:
                flash("You must be logged in", category="warning")
                return redirect(url_for('item.itemforsale', id=vendoritem.id))
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
                    return redirect(url_for('item.itemforsale', id=vendoritem.id))
                else:
                    return redirect(url_for('item.itemforsale', id=vendoritem.id))
            else:
                return redirect(url_for('item.itemforsale', id=vendoritem.id))

        else:
            return redirect(url_for('item.itemforsale', id=vendoritem.id))

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
                return redirect(url_for('checkout.shoppingcart', username=current_user.username))
            else:
                return redirect(url_for('checkout.shoppingcart', username=current_user.username))
        except Exception:
            return redirect(url_for('checkout.shoppingcart', username=current_user.username))
    except:
        return redirect(url_for('index', username=current_user.username))


@item.route('/saveforlater/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def savecartitem(id):
    try:
        user = db.session\
            .query(User)\
            .filter_by(username=current_user.username)\
            .first()
        try:
            item = ShoppingCart.query.get(id)
            if item.customer_id == user.id:
                item.savedforlater = 1
                db.session.add(item)
                db.session.commit()
                return redirect(url_for('checkout.shoppingcart', username=current_user.username))
            else:
                return redirect(url_for('checkout.shoppingcart', username=current_user.username))
        except Exception:
            return redirect(url_for('checkout.shoppingcart', username=current_user.username))
    except:
        return redirect(url_for('index', username=current_user.username))


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
                return redirect(url_for('checkout.shoppingcart', username=current_user.username))
            else:
                return redirect(url_for('checkout.shoppingcart', username=current_user.username))
        except Exception:
            return redirect(url_for('checkout.shoppingcart', username=current_user.username))
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
                            return redirect(url_for('checkout.shoppingcart', username=current_user.username))

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
                return redirect(url_for('checkout.shoppingcart,', username=current_user.username))
            else:
                flash("Item is not available.", category="success")
                return redirect(url_for('index', username=current_user.username))
        else:
            flash("Item is not available.", category="success")
            return redirect(url_for('index', username=current_user.username))
    except Exception as e:
        return redirect(url_for('index', username=current_user.username))
