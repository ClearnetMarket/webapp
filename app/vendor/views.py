from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
import shutil
import os
import csv
from app.vendor import vendor
from app import UPLOADED_FILES_DEST
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from decimal import Decimal
from sqlalchemy import func
from flask_paginate import Pagination, get_page_args
from app.achievements.v import obtainedtrustlevel
from app.exppoints import exppoint
from app.common.decorators import \
    website_offline, \
    login_required, \
    ping_user, \
    vendoraccount_required
from app.vendor.images.item_image_resizer import imagespider
from app.common.functions import \
    mkdir_p, \
    id_generator_picture1, \
    btc_cash_convertlocaltobtc, \
    itemlocation
# forms
from app.vendor.forms import \
    deactive, \
    ratingsForm, \
    feedbackcomment, \
    addtempreturn, \
    vendorleavereview, \
    vendorVerify, \
    add_product_form_factory, \
    addShipping, \
    ConfirmCancel, \
    UploadEbayForm

from app.userdata.views import \
    addtotalItemsBought, \
    addtotalItemsSold, \
    differenttradingpartners_user, \
    differenttradingpartners_vendor, \
    totalspentonitems_btccash, \
    vendortotalmade_btccash

from app.notification import notification

from app.search.searchfunction import headerfunctions_vendor
from app.wallet_bch.wallet_btccash_work import \
    btc_cash_sendCointoclearnet, \
    btc_cash_sendCointoUser, \
    btc_cash_sendCoinfromHoldings,\
    btc_cash_sendCointoHoldings

# models
from app.classes.achievements import \
    UserAchievements
from app.classes.auth import User

from app.classes.item import \
    marketItem

from app.classes.profile import \
    Userreviews, \
    Feedbackcomments

from app.classes.service import \
    shippingSecret, \
    Returns, \
    ReturnsTracking, \
    DefaultReturns, \
    Tracking

from app.classes.userdata import \
    Feedback

from app.classes.vendor import \
    Orders, \
    vendorVerification, \
    EbaySearchItem

from app.classes.wallet_bch import \
    *
from app.vendor.images.image_forms import image1, image2, image3, image4, image5
# End Models


@vendor.route('/trade-options/')
@website_offline
@login_required
@ping_user
@vendoraccount_required
def tradeOptions():
    """
    Returns the page with buttons to post type of item/ad
    :return:
    """
    return render_template('/vendor/tradeoptions.html')


@vendor.route('/myitems', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def itemsforSale():
    """
    Provides the vendors item list.
    Checks for incorrect listings and turns them off accordingly.
    Provides routing to edit, preview, delete item
    :return:
    """
    form = deactive(request.form)
    user, \
        order, \
        issues, \
        getnotifications, \
        customerdisputes \
        = headerfunctions_vendor()

    # Pagination
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args()
    # PEr Page tells how many search results pages
    inner_window = 5  # search bar at bottom used for .. lots of pages
    outer_window = 5  # search bar at bottom used for .. lots of pages
    per_page = 10
    # End Pagination
    # Query all the items related to the vendor
    sale = db.session.query(marketItem)
    sale = sale.filter(marketItem.vendor_id == user.id)
    forsale = sale.limit(per_page).offset(offset)

    pagination = Pagination(page=page,
                            total=sale.count(),
                            search=search,
                            record_name='items',
                            offset=offset,
                            per_page=per_page,
                            css_framework='bootstrap4',
                            inner_window=inner_window,
                            outer_window=outer_window)

    if request.method == "POST":
        if current_user.vacation == 0:
            see_if_changes = []
            for v in request.form.getlist('checkit'):
                intv = int(v)
                specific_item = db.session\
                    .query(marketItem)\
                    .filter_by(id=intv)\
                    .first()
                try:
                    if specific_item.vendor_id == current_user.id:

                        if specific_item.online == 0:
                            specific_item.online = 1
                            db.session.add(specific_item)
                            see_if_changes.append(1)
                        elif specific_item.online == 1:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            see_if_changes.append(1)
                        else:
                            pass

                        # Warnings
                        if len(specific_item.keywords) < 20:
                            flash("Item#" + str(specific_item.id) +
                                  ": Doesnt have very good keywords",
                                  category="warning")
                            see_if_changes.append(1)
                        # Turn off
                        if len(specific_item.imageone) < 10:
                            specific_item.online = 0
                            db.session.add(specific_item)

                            flash("Item#" + str(specific_item.id) +
                                  ": Doesnt have a main image", category="danger")
                            see_if_changes.append(1)
                        if specific_item.destinationcountry == '0':
                            specific_item.online = 0
                            db.session.add(specific_item)

                            flash("Item#" + str(specific_item.id) +
                                  ": Doesnt have a destination country",
                                  category="danger")
                            see_if_changes.append(1)
                        if specific_item.origincountry == '0':
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash("Item#" + str(specific_item.id) +
                                  ": Doesnt have an origin ", category="danger")
                            see_if_changes.append(1)

                        if specific_item.itemcount <= 0:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash("Item#" + str(specific_item.id) +
                                  ": Has been Sold out.  Update quantity to re-list it.",
                                  category="danger")
                            see_if_changes.append(1)

                        # needs price
                        if Decimal(specific_item.price) < .000001:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash("Item#" + str(specific_item.id) +
                                  ": Doesnt have a proper price", category="danger")
                            see_if_changes.append(1)
                        if len(specific_item.itemtitlee) < 10:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash("Item#" + str(specific_item.id) +
                                  ": Doesnt have a proper title", category="danger")
                            see_if_changes.append(1)

                        if specific_item.shippingtwo == 1:
                            if Decimal(specific_item.shippingprice2) > .01:
                                if len(specific_item.shippinginfo2) >= 2:
                                    pass
                            else:
                                specific_item.shippingtwo = 0
                                db.session.add(specific_item)
                                flash("Item#" + str(specific_item.id) +
                                      ": Doesnt have a proper shipping price 2",
                                      category="danger")
                                see_if_changes.append(1)

                        if specific_item.shippingthree == 1:
                            if Decimal(specific_item.shippingprice3) > .01:
                                if len(specific_item.shippinginfo3) >= 2:
                                    pass
                            else:
                                specific_item.shippingthree = 0
                                db.session.add(specific_item)
                                flash("Item#" + str(specific_item.id) +
                                      ": Doesnt have a proper shipping info 3 or price",
                                      category="danger")
                                see_if_changes.append(1)

                        if specific_item.shippingfree == 0 \
                                and specific_item.shippingtwo == 0 \
                                and specific_item.shippingthree == 0:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash("Item#" + str(specific_item.id) +
                                  ": Doesnt have a shipping method selected/checked",
                                  category="danger")
                            see_if_changes.append(1)

                except Exception as e:
                    print(str(e))
                    flash("Form Error", category="danger")
                    specific_item.online = 0
                    db.session.add(specific_item)
                    db.session.commit()

            if len(see_if_changes) > 0:
                db.session.commit()
        else:
            flash("You are currently on vacation mode.  Cannot put items online", category="danger")

    return render_template('/vendor/itemsforsale/vendorItemsforsale.html',
                           form=form,
                           forsale=forsale,
                           pagination=pagination,
                           user=user,
                           order=order,
                           issues=issues,
                           getnotifications=getnotifications,
                           customerdisputes=customerdisputes
                           )


@vendor.route('/create-an-item', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def createItem():
    """
    Vendor creates an item to be listed
    :return:
    """
    now = datetime.utcnow()
    # first see if they arnt spamming the site.  In future set to balance or level
    # current total items to prevent scripters
    gettotalitems = db.session.query(marketItem).filter_by(vendor_id=current_user.id).count()
    if gettotalitems < 100:
        # item = 0 creating item       item = 1 editing item
        vendorcreateItem = add_product_form_factory(item=0)
        form = vendorcreateItem(CombinedMultiDict((request.files, request.form)))

        user = db.session\
            .query(User)\
            .filter_by(username=current_user.username)\
            .first()

        if request.method == 'POST' and user.vendor_account == 1:
            if form.validate_on_submit():

                # Boolean fields
                if form.shippingtwo.data is True:
                    shippingtwo = 1
                else:
                    shippingtwo = 0

                if form.shippingthree.data is True:
                    shippingthree = 1
                else:
                    shippingthree = 0

                if form.return_this_item.data is True:
                    return_allowed = 1
                else:
                    return_allowed = 0

                if form.btc_accepted.data is True:
                    digital_currency2 = 1
                else:
                    digital_currency2 = 0

                if form.btc_cash_accepted.data is True:
                    digital_currency3 = 1
                else:
                    digital_currency3 = 0

                # Selectfield entries
                # Get currency from query
                currencyfull = form.currency.data
                cur = currencyfull.code

                # get item condition query
                itemconditionfull = form.itemcondition.data
                itemcondition = itemconditionfull.value

                # get itemcount query
                itemcountfull = form.itemcount.data
                itemcount = itemcountfull.value

                # get origin country query
                origincountryfull = form.origincountry.data
                origincountry = origincountryfull.numericcode

                # get destination 1
                getdest1full = form.destination1.data
                getdest1 = getdest1full.numericcode

                # get destination2
                getdest2full = form.destination2.data
                getdest2 = getdest2full.numericcode

                # getdestination 3
                getdest3full = form.destination3.data
                getdest3 = getdest3full.numericcode

                # getdestination 4
                getdest4full = form.destination4.data
                getdest4 = getdest4full.numericcode

                # getdestination 5
                getdest5full = form.destination5.data
                getdest5 = getdest5full.numericcode

                # get get not shipping 1
                getnotship1full = form.notshipping1.data
                getnotship1 = getnotship1full.value

                # get get not shipping 2
                getnotship2full = form.notshipping2.data
                getnotship2 = getnotship2full.value

                # get get not shipping 3
                getnotship3full = form.notshipping3.data
                getnotship3 = getnotship3full.value

                # get get not shipping 4
                getnotship4full = form.notshipping1.data
                getnotship4 = getnotship4full.value

                # get get not shipping 5
                getnotship5full = form.notshipping5.data
                getnotship5 = getnotship5full.value

                # get get not shipping 6
                getnotship6full = form.notshipping6.data
                getnotship6 = getnotship6full.value

                # get shippindayleast 0
                getshipdayleastfull0 = form.shippingdayleast0.data
                getshipdayleast0 = getshipdayleastfull0.value

                # get shipping day most 0
                getshippingdaymostfull0 = form.shippingdaymost0.data
                getshippingdaymost0 = getshippingdaymostfull0.value

                # get shippindayleast 2
                getshipdayleastfull2 = form.shippingdayleast2.data
                getshipdayleast2 = getshipdayleastfull2.value

                # get shipping day most 2
                getshippingdaymostfull2 = form.shippingdaymost2.data
                getshippingdaymost2 = getshippingdaymostfull2.value

                # get shippindayleast 3
                getshipdayleastfull3 = form.shippingdayleast3.data
                getshipdayleast3 = getshipdayleastfull3.value

                # get shipping day most 3
                getshippingdaymostfull3 = form.shippingdaymost3.data
                getshippingdaymost3 = getshippingdaymostfull3.value

                # category query
                categoryfull = form.category.data
                cat0 = categoryfull.id
                categoryname0 = categoryfull.name

                # create image of item in database
                item = marketItem(
                    stringnodeid=1,
                    categoryname0=categoryname0,
                    categoryid0=cat0,
                    digital_currency1=0,
                    digital_currency2=digital_currency2,
                    digital_currency3=digital_currency3,
                    created=datetime.utcnow(),
                    vendor_name=current_user.username,
                    vendor_id=current_user.id,
                    origincountry=origincountry,
                    destinationcountry=getdest1,
                    destinationcountrytwo=getdest2,
                    destinationcountrythree=getdest3,
                    destinationcountryfour=getdest4,
                    destinationcountryfive=getdest5,
                    itemtitlee=form.itemtitlee.data,
                    itemcount=itemcount,
                    itemdescription=form.itemdescription.data,
                    itemrefundpolicy=form.itemrefundpolicy.data,
                    price=form.pricee.data,
                    currency=cur,
                    itemcondition=itemcondition,
                    totalsold=0,
                    keywords=form.keywords.data,
                    return_allowed=return_allowed,
                    shippingfree=form.shippingfree.data,
                    shippinginfo0=form.shippinginfo0.data,
                    shippingdayleast0=getshipdayleast0,
                    shippingdaymost0=getshippingdaymost0,
                    shippinginfo2=form.shippinginfo2.data,
                    shippingprice2=form.shippingprice2.data,
                    shippingdayleast2=getshipdayleast2,
                    shippingdaymost2=getshippingdaymost2,
                    shippinginfo3=form.shippinginfo3.data,
                    shippingprice3=form.shippingprice3.data,
                    shippingdayleast3=getshipdayleast3,
                    shippingdaymost3=getshippingdaymost3,
                    notshipping1=getnotship1,
                    notshipping2=getnotship2,
                    notshipping3=getnotship3,
                    notshipping4=getnotship4,
                    notshipping5=getnotship5,
                    notshipping6=getnotship6,
                    details=form.details.data,
                    details1=form.details1.data,
                    details1answer=form.details1answer.data,
                    details2=form.details2.data,
                    details2answer=form.details2answer.data,
                    details3=form.details3.data,
                    details3answer=form.details3answer.data,
                    details4=form.details4.data,
                    details4answer=form.details4answer.data,
                    details5=form.details5.data,
                    details5answer=form.details5answer.data,
                    details6=form.details6.data,
                    details6answer=form.details6answer.data,
                    details7=form.details7.data,
                    details7answer=form.details7answer.data,
                    details8=form.details8.data,
                    details8answer=form.details8answer.data,
                    details9=form.details9.data,
                    details9answer=form.details9answer.data,
                    details10=form.details10.data,
                    details10answer=form.details10answer.data,
                    shippingtwo=shippingtwo,
                    shippingthree=shippingthree,
                    viewcount=0,
                    itemrating=0,
                    reviewcount=0,
                    online=0,
                    aditem=0,
                    aditem_level=0,
                    aditem_timer=datetime.utcnow(),
                    amazonid=0,
                    amazon_last_checked=now,
                )
                # add image to database
                db.session.add(item)
                db.session.flush()

                # node location
                getitemlocation = itemlocation(x=item.id)
                item.stringnodeid = getitemlocation

                # Images
                getimagesubfolder = itemlocation(x=item.id)
                directoryifitemlisting = os.path.join(UPLOADED_FILES_DEST, "item", getimagesubfolder, (str(item.id)))
                mkdir_p(path=directoryifitemlisting)

                image1(formdata=form.imageone1.data, item=item, directoryifitemlisting=directoryifitemlisting)
                image2(formdata=form.imagetwo.data, item=item, directoryifitemlisting=directoryifitemlisting)
                image3(formdata=form.imagethree.data, item=item, directoryifitemlisting=directoryifitemlisting)
                image4(formdata=form.imagefour.data, item=item, directoryifitemlisting=directoryifitemlisting)
                image5(formdata=form.imagefive.data, item=item, directoryifitemlisting=directoryifitemlisting)

                if item.shippingprice2 is None:
                    item.shippingprice2 = 0

                if item.shippingprice3 is None:
                    item.shippingprice3 = 0

                if item.price is None:
                    item.price = 0

                # update item id location for pathing
                item.auctionid = item.id
                item.stringauctionid = '/' + str(item.id) + '/'

                # convert image sizes
                db.session.add(item)
                db.session.commit()

                flash("Created New Item ", category="success")
                return redirect(url_for('vendor.itemsforSale', username=current_user.username))

            return redirect(url_for('vendor.createItem', username=current_user.username))

        return render_template('/vendor/itemsforsale/createItem.html',
                               form=form,
                               user=user)
    else:
        flash("100 items max", category="danger")
        return redirect(url_for('vendor.itemsforSale', username=current_user.username))


@vendor.route('/vendor-edititem/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def editItem(id):
    """
    Edits a specific item given an id
    :param id:
    :return:
    """
    now = datetime.utcnow()
    item = db.session\
        .query(marketItem)\
        .filter_by(id=id)\
        .first()
    if item:
        user = db.session\
            .query(User)\
            .filter_by(id=current_user.id)\
            .first()
        if item.vendor_id == user.id:

            vendorcreateItem = add_product_form_factory(item=item)
            form = vendorcreateItem(
                digital_currency2=item.digital_currency2,
                digital_currency3=item.digital_currency2,
                itemtitlee=item.itemtitlee,
                itemdescription=item.itemdescription,
                itemrefundpolicy=item.itemrefundpolicy,
                pricee=item.price,
                currency=item.currency,
                itemcount=item.itemcount,
                origincountry=item.origincountry,
                destination1=item.destinationcountry,
                destination2=item.destinationcountrytwo,
                destination3=item.destinationcountrythree,
                destination4=item.destinationcountryfour,
                destination5=item.destinationcountryfive,
                itemcondition=item.itemcondition,
                keywords=item.keywords,
                return_this_item=item.return_allowed,
                shippingfree=item.shippingfree,
                shippinginfo0=item.shippinginfo0,
                shippingdayleast0=item.shippingdayleast0,
                shippingdaymost0=item.shippingdaymost0,
                shippinginfo2=item.shippinginfo2,
                shippingprice2=item.shippingprice2,
                shippingdayleast2=item.shippingdayleast2,
                shippingdaymost2=item.shippingdaymost2,
                shippinginfo3=item.shippinginfo3,
                shippingprice3=item.shippingprice3,
                shippingdayleast3=item.shippingdayleast3,
                shippingdaymost3=item.shippingdaymost3,
                notshipping1=item.notshipping1,
                notshipping2=item.notshipping2,
                notshipping3=item.notshipping3,
                notshipping4=item.notshipping4,
                notshipping5=item.notshipping5,
                notshipping6=item.notshipping6,
                details=item.details,
                details1=item.details1,
                details1answer=item.details1answer,
                details2=item.details2,
                details2answer=item.details2answer,
                details3=item.details3,
                details3answer=item.details3answer,
                details4=item.details4,
                details4answer=item.details4answer,
                details5=item.details5,
                details5answer=item.details5answer,
                details6=item.details6,
                details6answer=item.details6answer,
                details7=item.details7,
                details7answer=item.details7answer,
                details8=item.details8,
                details8answer=item.details8answer,
                details9=item.details9,
                details9answer=item.details9answer,
                details10=item.details10,
                details10answer=item.details10answer,
                shippingthree=item.shippingthree,
                shippingtwo=item.shippingtwo,
                amazonid=0,
                amazon_last_checked=now,
            )

            if request.method == 'POST' and user.vendor_account == 1 and form.validate_on_submit():

                if item.vendor_id == user.id:
                    # Image location
                    getimagesubfolder = itemlocation(x=item.id)
                    directoryifitemlisting = os.path.join(UPLOADED_FILES_DEST, "item", getimagesubfolder, (str(item.id)))
                    mkdir_p(path=directoryifitemlisting)

                    image1(formdata=form.imageone1.data, item=item, directoryifitemlisting=directoryifitemlisting)
                    image2(formdata=form.imagetwo.data, item=item, directoryifitemlisting=directoryifitemlisting)
                    image3(formdata=form.imagethree.data, item=item, directoryifitemlisting=directoryifitemlisting)
                    image4(formdata=form.imagefour.data, item=item, directoryifitemlisting=directoryifitemlisting)
                    image5(formdata=form.imagefive.data, item=item, directoryifitemlisting=directoryifitemlisting)

                    if form.shippingtwo.data is True:
                        shippingtwo = 1

                    else:
                        shippingtwo = 0

                    if form.shippingthree.data is True:
                        shippingthree = 1
                    else:
                        shippingthree = 0

                    if form.btc_cash_accepted.data is True:
                        digital_currency3 = 1
                    else:
                        digital_currency3 = 0

                    # get category and subcategory
                    categoryfull = form.category_edit.data
                    cat0 = categoryfull.id
                    categoryname0 = categoryfull.name

                    # Get currency from query
                    currencyfull = form.currency1.data
                    cur = currencyfull.code

                    # get item condition query
                    itemconditionfull = form.itemcondition_edit.data
                    itemcondition = itemconditionfull.value

                    # get iitemcount query
                    itemcountfull = form.itemcount_edit.data
                    itemcount = itemcountfull.value

                    # get origin country query
                    origincountryfull = form.origincountry1.data
                    origincountry = origincountryfull.numericcode

                    # get destination 1
                    getdest1full = form.destination11.data
                    getdest1 = getdest1full.numericcode

                    # get destination2
                    getdest2full = form.destination21.data
                    getdest2 = getdest2full.numericcode

                    # getdestination 3
                    getdest3full = form.destination31.data
                    getdest3 = getdest3full.numericcode

                    # getdestination 4
                    getdest4full = form.destination41.data
                    getdest4 = getdest4full.numericcode

                    # getdestination 5
                    getdest5full = form.destination51.data
                    getdest5 = getdest5full.numericcode

                    # get get not shipping 1
                    getnotship1full = form.notshipping11.data
                    getnotship1 = getnotship1full.value

                    # get get not shipping 2
                    getnotship2full = form.notshipping21.data
                    getnotship2 = getnotship2full.value

                    # get get not shipping 3
                    getnotship3full = form.notshipping31.data
                    getnotship3 = getnotship3full.value

                    # get get not shipping 4
                    getnotship4full = form.notshipping11.data
                    getnotship4 = getnotship4full.value

                    # get get not shipping 5
                    getnotship5full = form.notshipping51.data
                    getnotship5 = getnotship5full.value

                    # get get not shipping 6
                    getnotship6full = form.notshipping61.data
                    getnotship6 = getnotship6full.value

                    # get shippindayleast 0
                    getshipdayleastfull0 = form.shippingdayleast01.data
                    getshipdayleast0 = getshipdayleastfull0.value

                    # get shipping day most 0
                    getshippingdaymostfull0 = form.shippingdaymost01.data
                    getshippingdaymost0 = getshippingdaymostfull0.value

                    # get shippindayleast 2
                    getshipdayleastfull2 = form.shippingdayleast21.data
                    getshipdayleast2 = getshipdayleastfull2.value

                    # get shipping day most 2
                    getshippingdaymostfull2 = form.shippingdaymost21.data
                    getshippingdaymost2 = getshippingdaymostfull2.value

                    # get shippindayleast 3
                    getshipdayleastfull3 = form.shippingdayleast31.data
                    getshipdayleast3 = getshipdayleastfull3.value

                    # get shipping day most 3
                    getshippingdaymostfull3 = form.shippingdaymost31.data
                    getshippingdaymost3 = getshippingdaymostfull3.value

                    # FORM DATA
                    item.categoryname0 = categoryname0,
                    item.categoryid0 = cat0,
                    item.shippingtwo = shippingtwo,
                    item.shippingthree = shippingthree,
                    item.digital_currency1 = 0,
                    item.digital_currency2 = 0,
                    item.digital_currency3 = digital_currency3,
                    item.origincountry = origincountry,
                    item.destinationcountry = getdest1,
                    item.destinationcountrytwo = getdest2,
                    item.destinationcountrythree = getdest3,
                    item.destinationcountryfour = getdest4,
                    item.destinationcountryfive = getdest5,
                    item.itemcondition = itemcondition,
                    item.itemtitlee = form.itemtitlee.data,
                    item.itemcount = itemcount,
                    item.itemdescription = form.itemdescription.data,
                    item.itemrefundpolicy = form.itemrefundpolicy.data,
                    item.price = form.pricee.data,
                    item.currency = cur,
                    item.keywords = form.keywords.data,
                    item.return_allowed = form.return_this_item.data,
                    item.shippingfree = form.shippingfree.data,
                    item.shippinginfo0 = form.shippinginfo0.data,
                    item.shippingdayleast0 = getshipdayleast0,
                    item.shippingdaymost0 = getshippingdaymost0,
                    item.shippinginfo2 = form.shippinginfo2.data,
                    item.shippingprice2 = form.shippingprice2.data,
                    item.shippingdayleast2 = getshipdayleast2,
                    item.shippingdaymost2 = getshippingdaymost2,
                    item.shippinginfo3 = form.shippinginfo3.data,
                    item.shippingprice3 = form.shippingprice3.data,
                    item.shippingdayleast3 = getshipdayleast3,
                    item.shippingdaymost3 = getshippingdaymost3,
                    item.notshipping1 = getnotship1,
                    item.notshipping2 = getnotship2,
                    item.notshipping3 = getnotship3,
                    item.notshipping4 = getnotship4,
                    item.notshipping5 = getnotship5,
                    item.notshipping6 = getnotship6,
                    item.details1 = form.details1.data,
                    item.details1answer = form.details1answer.data,
                    item.details2 = form.details2.data,
                    item.details2answer = form.details2answer.data,
                    item.details3 = form.details3.data,
                    item.details3answer = form.details3answer.data,
                    item.details4 = form.details4.data,
                    item.details4answer = form.details4answer.data,
                    item.details5 = form.details5.data,
                    item.details5answer = form.details5answer.data,
                    item.details6 = form.details6.data,
                    item.details6answer = form.details6answer.data,
                    item.details7 = form.details7.data,
                    item.details7answer = form.details7answer.data,
                    item.details8 = form.details8.data,
                    item.details8answer = form.details8answer.data,
                    item.details9 = form.details9.data,
                    item.details9answer = form.details9answer.data,
                    item.details10 = form.details10.data,
                    item.details10answer = form.details10answer.data,

                    if form.details.data is False:
                        item.details = 0
                    else:
                        item.details = 1

                    if form.shippingfree.data is False:
                        item.shippingfree = 0
                    else:
                        item.shippingfree = 1

                    if form.return_this_item.data is True:
                        item.return_allowed = 1
                    else:
                        item.return_allowed = 0

                    db.session.add(item)
                    db.session.commit()

                    flash(f"Updated: Item #{str(item.id)}",  category="success")
                    return redirect(url_for('vendor.itemsforSale'))

            return render_template('/vendor/itemsforsale/editItem.html',
                                   form=form,
                                   item=item,
                                   user=user
                                   )
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@vendor.route('/deletevendoritem/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def deleteItem(id):
    """
    Delete all images and the item data from database
    :param id:
    :return:
    """
    ext1 = '_225x'

    item = marketItem.query.get(id)
    if item:
        if item.vendor_id == current_user.id:
            try:
                specific_folder = str(item.id)
                getitemlocation = itemlocation(x=item.id)
                link = 'item'
                spacer = '/'
                pathtofile1 = str(UPLOADED_FILES_DEST + spacer + link + spacer + getitemlocation + spacer + specific_folder + spacer + item.imageone)
                pathtofile2 = str(UPLOADED_FILES_DEST + spacer + link + spacer + getitemlocation + spacer + specific_folder + spacer + item.imagetwo)
                pathtofile3 = str(UPLOADED_FILES_DEST + spacer + link + spacer + getitemlocation + spacer + specific_folder + spacer + item.imagethree)
                pathtofile4 = str(UPLOADED_FILES_DEST + spacer + link + spacer + getitemlocation + spacer + specific_folder + spacer + item.imagefour)
                pathtofile5 = str(UPLOADED_FILES_DEST + spacer + link + spacer + getitemlocation + spacer + specific_folder + spacer + item.imagefive)

                try:
                    pathtofile1, file_extension1 = os.path.splitext(
                        pathtofile1)
                except:
                    pass

                try:
                    pathtofile2, file_extension2 = os.path.splitext(
                        pathtofile2)
                except:
                    pass

                try:
                    pathtofile3, file_extension3 = os.path.splitext(
                        pathtofile3)
                except:
                    pass
                try:
                    pathtofile4, file_extension4 = os.path.splitext( pathtofile4)
                except:
                    pass

                try:
                    pathtofile5, file_extension5 = os.path.splitext(
                        pathtofile5)
                except:
                    pass

                try:
                    delete_file_one = str(pathtofile1 + file_extension1)
                    delete_file_one_ext = str(
                        pathtofile1 + ext1 + file_extension1)
                except:
                    pass

                try:
                    delete_file_two = str(pathtofile2 + file_extension2)
                    delete_file_two_ext = str(
                        pathtofile2 + ext1 + file_extension2)
                except:
                    pass

                try:
                    delete_file_three = str(pathtofile3 + file_extension3)
                    delete_file_three_ext = str(
                        pathtofile3 + ext1 + file_extension3)
                except:
                    pass

                try:
                    delete_file_four = str(pathtofile4 + file_extension4)
                    delete_file_four_ext = str(
                        pathtofile4 + ext1 + file_extension4)
                except:
                    pass

                try:
                    delete_file_five = str(pathtofile5 + file_extension5)
                    delete_file_five_ext = str(
                        pathtofile5 + ext1 + file_extension5)

                except:
                    pass

                item_one_image = item.imageone
                if len(item_one_image) > 10:
                    try:
                        os.remove(delete_file_one)
                    except:
                        pass
                    try:
                        os.remove(delete_file_one_ext)
                    except:
                        pass

                else:
                    pass
                item_two_image = item.imagetwo
                if len(item_two_image) > 10:
                    try:
                        os.remove(delete_file_two)
                    except:
                        pass
                    try:
                        os.remove(delete_file_two_ext)
                    except:
                        pass

                else:
                    pass
                item_three_image = item.imagethree
                if len(item_three_image) > 10:
                    try:
                        os.remove(delete_file_three)
                    except:
                        pass
                    try:
                        os.remove(delete_file_three_ext)
                    except:
                        pass

                else:
                    pass
                item_four_image = item.imagefour
                if len(item_four_image) > 10:
                    try:
                        os.remove(delete_file_four)
                    except:
                        pass
                    try:
                        os.remove(delete_file_four_ext)
                    except:
                        pass
                else:
                    pass
                item_five_image = item.imagefive
                if len(item_five_image) > 10:
                    try:
                        os.remove(delete_file_five)
                    except:
                        pass
                    try:
                        os.remove(delete_file_five_ext)
                    except:
                        pass
                else:
                    pass

                db.session.delete(item)
                db.session.commit()
            except:
                return redirect(url_for('vendor.itemsforSale', username=current_user.username))
        else:
            return redirect(url_for('vendor.itemsforSale', username=current_user.username))
        return redirect(url_for('vendor.itemsforSale', username=current_user.username))
    else:
        flash("Error", category="danger")
        return redirect(url_for('index'))


@vendor.route('/clone-cloneitem/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def cloneItem(id):
    """
    given an item id, this will create a new folder on storage, and recopy the data with a new id
    :param id:
    :return:
    """
    # get the vendor item to be copied
    now = datetime.utcnow()
    vendoritem = marketItem.query.filter_by(id=id).first()
    if vendoritem:
        if vendoritem.vendor_id == current_user.id:
            # make sure user doesnt have to many auctions
            vendoritemcount = db.session\
                .query(marketItem)\
                .filter_by(vendor_id=current_user.id)\
                .count()
            if vendoritemcount < 1000:
                try:
                    priceDecimaled = Decimal(vendoritem.price)
                    p2 = Decimal(vendoritem.shippingprice2)
                    p3 = Decimal(vendoritem.shippingprice3)

                    Item = marketItem(
                        stringnodeid=vendoritem.stringnodeid,
                        created=datetime.utcnow(),
                        vendor_name=current_user.username,
                        vendor_id=current_user.id,
                        origincountry=vendoritem.origincountry,
                        destinationcountry=vendoritem.destinationcountry,
                        destinationcountrytwo=vendoritem.destinationcountrytwo,
                        destinationcountrythree=vendoritem.destinationcountrythree,
                        destinationcountryfour=vendoritem.destinationcountryfour,
                        destinationcountryfive=vendoritem.destinationcountryfive,
                        return_allowed=vendoritem.return_allowed,
                        itemtitlee=vendoritem.itemtitlee,
                        itemcount=0,
                        itemdescription=vendoritem.itemdescription,
                        itemrefundpolicy=vendoritem.itemrefundpolicy,
                        price=priceDecimaled,
                        currency=vendoritem.currency,
                        imageone=vendoritem.imageone,
                        imagetwo=vendoritem.imagetwo,
                        imagethree=vendoritem.imagethree,
                        imagefour=vendoritem.imagefour,
                        imagefive=vendoritem.imagefive,
                        itemcondition=vendoritem.itemcondition,
                        totalsold=0,
                        keywords=vendoritem.keywords,
                        shippingfree=vendoritem.shippingfree,
                        shippinginfo0=vendoritem.shippinginfo0,
                        shippingdayleast0=vendoritem.shippingdayleast0,
                        shippingdaymost0=vendoritem.shippingdaymost0,
                        shippinginfo2=vendoritem.shippinginfo2,
                        shippingprice2=p2,
                        shippingdayleast2=vendoritem.shippingdayleast2,
                        shippingdaymost2=vendoritem.shippingdaymost2,
                        shippinginfo3=vendoritem.shippinginfo3,
                        shippingprice3=p3,
                        shippingdayleast3=vendoritem.shippingdayleast3,
                        shippingdaymost3=vendoritem.shippingdaymost3,
                        notshipping1=vendoritem.notshipping1,
                        notshipping2=vendoritem.notshipping2,
                        notshipping3=vendoritem.notshipping3,
                        notshipping4=vendoritem.notshipping4,
                        notshipping5=vendoritem.notshipping5,
                        notshipping6=vendoritem.notshipping6,
                        details=vendoritem.details,
                        details1=vendoritem.details1,
                        details1answer=vendoritem.details1answer,
                        details2=vendoritem.details2,
                        details2answer=vendoritem.details2answer,
                        details3=vendoritem.details3,
                        details3answer=vendoritem.details3answer,
                        details4=vendoritem.details4,
                        details4answer=vendoritem.details4answer,
                        details5=vendoritem.details5,
                        details5answer=vendoritem.details5answer,
                        details6=vendoritem.details6,
                        details6answer=vendoritem.details6answer,
                        details7=vendoritem.details7,
                        details7answer=vendoritem.details7answer,
                        details8=vendoritem.details8,
                        details8answer=vendoritem.details8answer,
                        details9=vendoritem.details9,
                        details9answer=vendoritem.details9answer,
                        details10=vendoritem.details10,
                        details10answer=vendoritem.details10answer,
                        shippingtwo=vendoritem.shippingtwo,
                        shippingthree=vendoritem.shippingthree,
                        viewcount=0,
                        itemrating=0,
                        reviewcount=0,
                        online=0,
                        aditem=0,
                        aditem_level=0,
                        aditem_timer=datetime.utcnow(),
                        amazonid=0,
                        amazon_last_checked=now,
                        categoryname0=vendoritem.categoryname0,
                        categoryid0=vendoritem.categoryid0,
                        digital_currency1=0,
                        digital_currency2=1,
                        digital_currency3=0,
                    )
                    db.session.add(Item)
                    db.session.flush()

                    # IMAGES
                    # Make New image folder
                    getitemlocation = itemlocation(x=lastitemid)
                    listingdir = 'item/' + getitemlocation + \
                        '/' + str(Item.id) + '/'
                    mkdir_p(path=UPLOADED_FILES_DEST + listingdir)
                    # get old directory path
                    oldirectory = UPLOADED_FILES_DEST + "item/" + \
                        getitemlocation + '/' + str(vendoritem.id) + '/'
                    # new directory path
                    newdirectory = UPLOADED_FILES_DEST + listingdir
                    # lopp over the files and copy them
                    for file_name in os.listdir(oldirectory):
                        full_file_name = os.path.join(oldirectory, file_name)
                        if os.path.isfile(full_file_name):
                            shutil.copy(full_file_name, newdirectory)
                    # query the newly added item, and change the id's accordingly
                    Item.stringauctionid = '/' + str(Item.id) + '/'

                    getitemlocation = itemlocation(x=Item.id)
                    Item.stringnodeid = getitemlocation
                    db.session.add(Item)
                    db.session.commit()

                    flash("Cloned New Item ", category="success")
                    return redirect(url_for('vendor.itemsforSale'))

                except Exception as e:
                    flash(str(e), category="danger")
                    db.session.rollback()
                    flash("Error.  Could not clone", category="danger")
                    return redirect(url_for('index'))
            else:
                flash("Maximum 1000 items allowed per user. "
                      " This will change when leveling process is update."
                      "  Higher the level, more listings", category="success")
        else:
            flash("Error", category="danger")
            return redirect(url_for('index'))
    else:
        flash("Error", category="danger")
        return redirect(url_for('index'))


@vendor.route('/needavacation/', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vacation():
    """
    Vacation mode allows user to turn off all items instantly.  In the future
    add a message perhaps and keep items online
    :return:
    """
    # Turn off all items, and remove users visibility
    user = db.session\
        .query(User)\
        .filter_by(username=current_user.username)\
        .first()

    # get physical items
    aitems = db.session\
        .query(marketItem)\
        .filter(marketItem.vendor_id == current_user.id)\
        .all()

    if user.vacation == 0:
        # Go into vacation mode
        user.vacation = 1
        db.session.add(user)
        if aitems:
            for a in aitems:
                a.online = 0
                db.session.add(a)
        flash("Vacation mode on.  Items are taken offline", category="success")
    else:
        # Turn off vacation mode
        user.vacation = 0
        db.session.add(user)
        flash("Vacation mode off.  You Can put items online", category="success")
    db.session.commit()
    return redirect(url_for('auth.myAccount', username=current_user.username))


@vendor.route('/deletepicture/<int:id>/<string:img>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def deleteimg(id, img):
    """
    gets specific id and image, it will delete on the server accordingly
    :param id:
    :param img:
    :return:
    """
    try:
        vendoritem = db.session\
            .query(marketItem)\
            .filter_by(id=id)\
            .first()
        if vendoritem:
            if vendoritem.vendor_id == current_user.id:
                try:
                    specific_folder = str(vendoritem.id)

                    link = 'item'
                    spacer = '/'
                    pathtofile = str(UPLOADED_FILES_DEST + link +  spacer + specific_folder + spacer + img)
                    pathtofile, file_extension = os.path.splitext(pathtofile)

                    ext1 = '_225x'
                    ext_2 = '_500x'

                    file0 = str(pathtofile + file_extension)
                    file1 = str(pathtofile + ext1 + file_extension)

                    if len(img) > 20:
                        x1 = vendoritem.imageone
                        x2 = vendoritem.imagetwo
                        x3 = vendoritem.imagethree
                        x4 = vendoritem.imagefour
                        x5 = vendoritem.imagefive

                        if x1 == img:
                            vendoritem.imageone = '0'
                            db.session.add(vendoritem)

                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif x2 == img:
                            vendoritem.imagetwo = '0'
                            db.session.add(vendoritem)

                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif x3 == img:
                            vendoritem.imagethree = '0'
                            db.session.add(vendoritem)

                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif x4 == img:
                            vendoritem.imagefour = '0'
                            db.session.add(vendoritem)

                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif x5 == img:
                            vendoritem.imagefive = '0'
                            db.session.add(vendoritem)

                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        else:
                            return redirect(url_for('vendor.editItem', id=id))
                        db.session.commit()
                    return redirect(url_for('vendor.editItem', id=id))
                except Exception:
                    return redirect(url_for('vendor.editItem', id=id))
            else:
                return redirect(url_for('vendor.editItem', id=id))
        else:
            flash("Error", category="danger")
            return redirect(url_for('index'))
    except:
        return redirect(url_for('index', username=current_user.username))



def deleteimg_noredirect(id, img):
    try:
        vendoritem = marketItem.query.get(id)
        if vendoritem:
            if vendoritem.vendor_id == current_user.id:
                try:
                    specific_folder = str(vendoritem.id)

                    link = 'listing'
                    spacer = '/'
                    pathtofile = str(UPLOADED_FILES_DEST + link +
                                     spacer + specific_folder + spacer + img)
                    pathtofile, file_extension = os.path.splitext(pathtofile)

                    ext1 = '_225x'

                    file0 = str(pathtofile + file_extension)
                    file1 = str(pathtofile + ext1 + file_extension)

                    if len(img) > 20:
                        x1 = vendoritem.imageone
                        x2 = vendoritem.imagetwo
                        x3 = vendoritem.imagethree
                        x4 = vendoritem.imagefour
                        x5 = vendoritem.imagefive

                        if x1 == img:
                            vendoritem.imageone = '0'
                            db.session.add(vendoritem)
                            db.session.commit()
                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif x2 == img:
                            vendoritem.imagetwo = '0'
                            db.session.add(vendoritem)
                            db.session.commit()
                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif x3 == img:
                            vendoritem.imagethree = '0'
                            db.session.add(vendoritem)
                            db.session.commit()
                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif x4 == img:
                            vendoritem.imagefour = '0'
                            db.session.add(vendoritem)
                            db.session.commit()
                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif x5 == img:
                            vendoritem.imagefive = '0'
                            db.session.add(vendoritem)
                            db.session.commit()
                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        else:
                            pass

                except Exception:
                    flash("Error", category="danger")
                    return redirect(url_for('index'))
        else:
            flash("Error", category="danger")
            return redirect(url_for('index'))
    except:
        return redirect(url_for('index', username=current_user.username))


@vendor.route('/vendor-accept/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorOrders_accept(id):
    try:
        item = Orders.query.get(id)
        if item is not None:
            if item.vendor_id == current_user.id and item.vendor_id != 0 and item.released == 0:
                try:
                    item.new_order = 0
                    item.accepted_order = 1
                    item.age = datetime.utcnow()
                    db.session.add(item)
                    db.session.commit()
                    flash("Order Accepted", category="success")
                    return redirect(url_for('vendor.vendorOrders', username=current_user.username))
                except Exception:
                    return redirect(url_for('vendor.vendorOrders', username=current_user.username))
            else:
                return redirect(url_for('vendor.vendorOrders', username=current_user.username))
        else:
            flash("Error.  Item doesnt exist", category="danger")
            return redirect(url_for('index'))

    except:
        return redirect(url_for('index', username=current_user.username))


@vendor.route('/vendor-send/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorOrders_send(id):
    try:
        item = Orders.query.get(id)
        if item:
            if item.vendor_id == current_user.id \
                    and item.vendor_id != 0 \
                    and item.released == 0:
                try:
                    item.accepted_order = 0
                    item.request_cancel = 0
                    item.waiting_order = 1
                    item.reason_cancel = 0
                    db.session.add(item)
                    db.session.commit()
                    flash("Order Shipped", category="success")
                    return redirect(url_for('vendor.vendorOrders', username=current_user.username))
                except Exception:
                    return redirect(url_for('vendor.vendorOrders', username=current_user.username))
            else:
                return redirect(url_for('vendor.vendorOrders', username=current_user.username))
        else:
            flash("Error", category="danger")
            return redirect(url_for('index'))

    except:
        return redirect(url_for('index', username=current_user.username))


@vendor.route('/vendor-dispute/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorOrders_dispute(id):
    try:
        item = Orders.query.get(id)
        if item.vendor_id == current_user.id:
            try:
                item.disputed_order = 1
                db.session.add(item)
                db.session.commit()
                flash("Item Disputed", category="success")
                return redirect(url_for('service.customerservice_dispute', username=current_user.username))
            except Exception:
                return redirect(url_for('service.customerservice_dispute', username=current_user.username))
        else:
            return redirect(url_for('service.customerservice_dispute', username=current_user.username))
    except:
        return redirect(url_for('index', username=current_user.username))


@vendor.route('/customer-dispute/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def customerOrders_dispute(id):
    item = Orders.query.get(id)
    if item:
        try:
            if item.vendor_id == current_user.id or item.customer_id == current_user.id:
                item.disputed_order = 1
                db.session.add(item)
                db.session.commit()
                flash("Item Disputed", category="success")
                return redirect(url_for('service.customerservice_dispute', username=current_user.username))
            else:
                return redirect(url_for('index', username=current_user.username))
        except:
            return redirect(url_for('index', username=current_user.username))
    else:
        flash("Error", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-reject/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorOrders_reject(id):
    now = datetime.utcnow()
    item = Orders.query.get(id)
    if item:
        try:
            msg = db.session\
                .query(shippingSecret)\
                .filter_by(orderid=id)\
                .first()
            gettracking = db.session\
                .query(Tracking)\
                .filter_by(sale_id=id)\
                .first()
            if item.vendor_id == current_user.id and item.released == 0 and item.vendor_id != 0:
                if item.completed == 0:
                    try:
                        item.cancelled = 1
                        item.completed = 1
                        item.completed_time = now
                        item.disputed_order = 0
                        item.request_cancel = 0
                        item.waiting_order = 0
                        item.delivered_order = 0
                        item.new_order = 0
                        item.accepted_order = 0

                        db.session.add(item)
                        db.session.flush()

                        # calculate how much to refund(shipping and price)
                        the_item_price = item.price
                        the_item_shipping_price = item.shipping_price
                        if the_item_shipping_price:
                            the_item_shipping_price = the_item_shipping_price
                        else:
                            the_item_shipping_price = 0
                        refund = Decimal(the_item_price) + \
                            Decimal(the_item_shipping_price)

                        btc_cash_sendCointoUser(amount=refund,
                                                comment=item.id,
                                                user_id=item.vendor_id,
                                                )
                        # delete shipping message
                        if msg:
                            db.session.delete(msg)
                        # delete tracking
                        if gettracking:
                            db.session.delete(gettracking)
                        # change the quantity
                        if item.type == 1:
                            getitem = db.session.query(marketItem).filter(
                                item.item_id == marketItem.id).first()
                            x = getitem.itemcount
                            y = item.quantity
                            z = x + y
                            getitem.itemcount = z
                            db.session.add(getitem)

                        notification(type=7, username=item.customer,
                                     user_id=item.customer_id, salenumber=item.id, bitcoin=0)
                        flash("Order Cancelled", category="danger")
                        db.session.commit()
                        return redirect(url_for('vendor.vendorOrders', username=current_user.username))
                    except Exception as e:
                        flash("Error", category="danger")
                        return redirect(url_for('vendor.vendorOrders', username=current_user.username))
                else:
                    flash("Error", category="danger")
                    return redirect(url_for('vendor.vendorOrders', username=current_user.username))
            else:
                return redirect(url_for('vendor.vendorOrders', username=current_user.username))
        except Exception as e:
            return redirect(url_for('index', username=current_user.username))
    else:
        flash("Error", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-cancelandrefund/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorOrders_cancelandrefund(id):
    now = datetime.utcnow()
    item = Orders.query.get(id)
    if item:

        msg = db.session\
            .query(shippingSecret)\
            .filter_by(orderid=id)\
            .first()
        gettracking = db.session\
            .query(Tracking)\
            .filter_by(sale_id=id)\
            .first()

        if item.vendor_id == current_user.id:
            if item.released == 0 and item.cancelled == 0 and item.vendor_id != 0:
                try:
                    p = item.price
                    s = item.shipping_price
                    refund = Decimal(p) + Decimal(s)

                    item.cancelled = 1
                    item.completed = 1
                    item.request_cancel = 0
                    item.completed_time = now
                    item.disputed_order = 0
                    item.waiting_order = 0
                    item.delivered_order = 0
                    item.new_order = 0
                    item.accepted_order = 0

                    db.session.add(item)

                    notification(type=7,
                                 username=item.customer,
                                 user_id=item.customer_id,
                                 salenumber=item.id,
                                 bitcoin=0)

                    btc_cash_sendCointoUser(amount=refund,
                                            comment=item.id,
                                            user_id=item.vendor_id,
                                            )

                    # Give user neg exp
                    exppoint(user=item.customer_id,
                             price=0,
                             type=9,
                             quantity=0,
                             currency=0)
                    if msg:
                        db.session.delete(msg)
                    if gettracking:
                        db.session.delete(gettracking)
                    flash("Order Cancelled", category="danger")
                    db.session.commit()
                    return redirect(url_for('vendor.vendorOrders', username=current_user.username))
                except Exception as e:
                    return redirect(url_for('vendor.vendorOrders', username=current_user.username))
            else:
                flash("Error.  Cancelled already.", category="danger")
                return redirect(url_for('vendor.vendorOrders', username=current_user.username))
        else:
            flash("Vendor id doesnt equal user id", category="danger")
            return redirect(url_for('vendor.vendorOrders', username=current_user.username))
    else:
        flash("Error", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-leavereviewforuser/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def vendorOrders_leavereviewforuser(id):
    now = datetime.utcnow()
    form = vendorleavereview()
    order = db.session.query(Orders).filter_by(id=id).first()
    if order:
        if order.vendor_id == current_user.id:
            userreviews = db.session\
                .query(Userreviews)\
                .filter(Userreviews.customer_id == order.customer_id)\
                .order_by(Userreviews.dateofreview.desc())\
                .limit(20)

            item = db.session\
                .query(marketItem)\
                .filter(marketItem.id == order.item_id)\
                .first()

            if request.method == "POST" and form.validate_on_submit():
                if order.cancelled == 0:
                    try:
                        text_box_value_userrating = request.form.get(
                            "itemrating")
                        text_box_value_comment = request.form.get(
                            "reviewcomment")

                        add_feedback = Userreviews(
                            order_id=order.id,
                            customer=order.customer,
                            customer_id=order.customer_id,
                            review=text_box_value_comment,
                            dateofreview=datetime.utcnow(),
                            rating=text_box_value_userrating,
                        )
                        db.session.add(add_feedback)
                        order.userfeedback = 1

                        db.session.add(order)

                        exppoint(user=order.vendor_id,
                                 price=0,
                                 type=2,
                                 quantity=int(text_box_value_userrating),
                                 currency=0)
                        exppoint(user=order.customer_id,
                                 price=0,
                                 type=6,
                                 quantity=int(text_box_value_userrating),
                                 currency=0)
                        db.session.commit()
                        flash('Feedback submitted.  Exp Points Given..', 'success ')
                        return redirect(url_for('vendor.vendorOrders_leavereviewforuser', id=id))

                    except Exception as e:
                        return redirect(url_for('vendor.vendorOrders_leavereviewforuser', id=id))
                else:
                    flash('Cant leave Feedback.  Order was cancelled', 'danger ')
                    return redirect(url_for('vendor.vendorOrders_leavereviewforuser', id=id))

            return render_template('/vendor/leavecustomerreview.html',
                                   username=current_user.username,
                                   order=order,
                                   userreviews=userreviews,
                                   item=item,
                                   form=form,
                                   now=now)
        else:
            return redirect(url_for('vendor.Orders'))
    else:
        return redirect(url_for('vendor.Orders'))


@vendor.route('/vendor-deleteorderhistory/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorOrders_deleteorderhistory(id):

    try:
        item = Orders.query.get(id)
        if item.vendor_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
            flash("Order Deleted", category="success")
            if item.type == 3:
                return redirect(url_for('vendor.vendoropenTrades', username=current_user.username))
            elif item.type == 2:
                return redirect(url_for('vendor.vendoropenTrades', username=current_user.username))
            else:
                return redirect(url_for('vendor.vendorOrders', username=current_user.username))
        else:
            return redirect(url_for('index', username=current_user.username))
    except:
        flash("Order Deletion error.  Please send feedback/bug", category="danger")
        return redirect(url_for('index', username=current_user.username))


@vendor.route('/vendor-addtracking/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorOrders_addtracking(id):
    itemcustomer = db.session\
        .query(Orders)\
        .filter_by(id=id)\
        .first()
    if itemcustomer.vendor_id == current_user.id:
        tracking = db.session.query(Tracking).filter_by(sale_id=id).first()
        if tracking:
            form = addShipping(
                sale_id=itemcustomer.id,
                trackingnumber1=tracking.tracking1,
                selectcarrier1=tracking.carrier1,
                othercarrier1=tracking.othercarrier1,
                trackingnumber2=tracking.tracking2,
                selectcarrier2=tracking.carrier2,
                othercarrier2=tracking.othercarrier2,
                trackingnumber3=tracking.tracking3,
                selectcarrier3=tracking.carrier3,
                othercarrier3=tracking.othercarrier3
            )
            if request.method == 'POST' and form.validate_on_submit():
                car1full = form.selectcarrier1.data
                car1 = car1full.value
                car2full = form.selectcarrier2.data
                car2 = car2full.value
                car3full = form.selectcarrier3.data
                car3 = car3full.value
                if (0 <= car1 <= 4) and (0 <= car2 <= 4) and (0 <= car3 <= 4):
                    tracking.sale_id = itemcustomer.id,
                    tracking.tracking1 = form.trackingnumber1.data,
                    tracking.carrier1 = car1,
                    tracking.othercarrier1 = form.othercarrier1.data,
                    tracking.tracking2 = form.trackingnumber2.data,
                    tracking.carrier2 = car2,
                    tracking.othercarrier2 = form.othercarrier2.data,
                    tracking.tracking3 = form.trackingnumber3.data,
                    tracking.carrier3 = car3,
                    tracking.othercarrier3 = form.othercarrier3.data,

                    db.session.add(tracking)
                    db.session.commit()
                    return redirect(url_for('vendor.vendorOrders', username=current_user.username))

            return render_template('/vendor/addtracking.html', username=current_user.username, form=form)
        else:
            form = addShipping(request.form)
            if request.method == 'POST' and form.validate_on_submit():

                car1full = form.selectcarrier1.data
                car1 = car1full.value

                car2full = form.selectcarrier2.data
                car2 = car2full.value

                car3full = form.selectcarrier3.data
                car3 = car3full.value

                if (0 <= car1 <= 4) and (0 <= car2 <= 4) and (0 <= car3 <= 4):
                    theitem = Tracking(
                        sale_id=itemcustomer.id,
                        tracking1=form.trackingnumber1.data,
                        carrier1=car1,
                        othercarrier1=form.othercarrier1.data,
                        tracking2=form.trackingnumber2.data,
                        carrier2=car2,
                        othercarrier2=form.othercarrier2.data,
                        tracking3=form.trackingnumber3.data,
                        carrier3=car3,
                        othercarrier3=form.othercarrier3.data,
                    )

                    db.session.add(theitem)
                    db.session.commit()

                    return redirect(url_for('vendor.vendorOrders', username=current_user.username))
            return render_template('/vendor/addtracking.html', username=current_user.username, form=form)
    else:
        flash("Cannot view Info.", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-reasonforcancel/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorOrders_reasonforcancel(id):
    item = db.session.query(Orders).filter_by(id=id).first()
    if item.vendor_id == current_user.id:
        return render_template('/vendor/reasontocancel.html', item=item)
    else:
        flash("Cannot view Order.", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-ratings', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorRatings():
    now = datetime.utcnow()
    form = ratingsForm(request.form)
    user, \
        order, \
        issues, \
        getnotifications, \
        customerdisputes \
        = headerfunctions_vendor()

    getavgitem = db.session.query(
        func.avg(Feedback.itemrating).label("avgitem"))
    getavgitem = getavgitem.filter(Feedback.vendorid == user.id)
    gitem = getavgitem.all()
    itemscore = str((gitem[0][0]))[:4]

    getavgvendor = db.session.query(
        func.avg(Feedback.vendorrating).label("avgvendor"))
    getavgvendor = getavgvendor.filter(Feedback.vendorid == user.id)
    gvendor = getavgvendor.all()
    vendorscore = str((gvendor[0][0]))[:4]

    if vendorscore is None:
        vendorscore = 0
    else:
        vendorscore = vendorscore

    if itemscore is None:
        itemscore = 0
    else:
        itemscore = itemscore

    # Pagination
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args()
    # PEr Page tells how many search results pages
    inner_window = 5  # search bar at bottom used for .. lots of pages
    outer_window = 5  # search bar at bottom used for .. lots of pages
    per_page = 25
    # end pagination

    ratings = db.session\
        .query(Feedback)\
        .filter_by(vendorid=current_user.id)\
        .order_by(Feedback.timestamp.desc())
    ratings = ratings.limit(per_page).offset(offset)

    pagination = Pagination(page=page,
                            total=ratings.count(),
                            search=search,
                            record_name='ratings',
                            offset=offset,
                            per_page=per_page,
                            css_framework='bootstrap5',
                            inner_window=inner_window,
                            outer_window=outer_window)

    if request.method == 'POST':
        ratingdata = form.sortrating.data

        if ratingdata == '0':
            pass
        elif ratingdata == '1':
            # Newest ratings first
            r = db.session.query(Feedback)
            r = r.filter_by(vendorid=user.id)
            r = r.order_by(Feedback.timestamp.desc())
            ratings = r.limit(per_page).offset(offset)

        elif ratingdata == '2':
            # Highest vendor ratings first
            r = db.session.query(Feedback)
            r = r.filter_by(vendorid=user.id)
            r = r.order_by(Feedback.vendorrating.desc())
            ratings = r.limit(per_page).offset(offset)

        elif ratingdata == '3':
            # Highest vendor ratings first
            r = db.session.query(Feedback)
            r = r.filter_by(vendorid=user.id)
            r = r.order_by(Feedback.vendorrating.asc())
            ratings = r.limit(per_page).offset(offset)
        else:
            flash("Invalid Selection.", category="danger")
            return redirect(url_for('index'))

    return render_template('/vendor/vendorRatings.html',
                           user=user, now=now,
                           form=form,
                           ratings=ratings,
                           itemscore=itemscore,
                           vendorscore=vendorscore,
                           pagination=pagination,
                           order=order,
                           issues=issues,
                           getnotifications=getnotifications,
                           customerdisputes=customerdisputes
                           )


@vendor.route('/vendor-viewfeedbackspecific/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
def vendorviewspecificfeedback(id):
    try:
        now = datetime.utcnow()
        form = feedbackcomment(request.form)

        user = db.session\
            .query(User)\
            .filter_by(username=current_user.username)\
            .first()
        rating = db.session\
            .query(Feedback)\
            .filter_by(id=id)\
            .first()
        ileftfeedback = db.session\
            .query(Feedbackcomments)\
            .filter_by(feedback_id=id)\
            .first()
        order = db.session\
            .query(Orders)\
            .filter_by(id=rating.sale_id)\
            .first()
        if order is not None:
            if order.vendor_id == current_user.id:
                return render_template('/vendor/viewspecificfeedback.html',
                                       user=user, now=now,
                                       ileftfeedback=ileftfeedback,
                                       rating=rating,
                                       form=form,
                                       order=order)
            else:
                flash("Cannot view Order.", category="danger")
                return redirect(url_for('index'))
        else:
            flash("Order doesnt exist.", category="danger")
            return redirect(url_for('index'))

    except Exception as e:
        flash("Feedback on order error.", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vieworder/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
def viewOrder(id):
    order = db.session.query(Orders).filter_by(id=id).first()
    if order:
        if order.customer_id == current_user.id or order.vendor_id == current_user.id or current_user.admin_role <= 3:
            if current_user.id == order.vendor_id and order.request_return == 1:
                return redirect(url_for('vendor.addtempaddress', id=id))

            if current_user.id == order.customer_id and order.request_return == 2:
                return redirect(url_for('auth.customerOrders_returninstructions', id=id))
            else:

                tracking = db.session\
                    .query(Tracking)\
                    .filter_by(sale_id=id)\
                    .first()
                getitem = db.session\
                    .query(marketItem)\
                    .filter(marketItem.id == order.item_id)\
                    .first()
                # delete return address
                returninfo = db.session\
                    .query(Returns)\
                    .filter_by(ordernumber=id)\
                    .first()
                returns = db.session\
                    .query(Returns)\
                    .filter_by(ordernumber=order.id)\
                    .first()
                # delete return tracking
                returntracking = db.session\
                    .query(ReturnsTracking)\
                    .filter_by(ordernumber=id)\
                    .first()
                vendortracking = db.session\
                    .query(Tracking)\
                    .filter_by(sale_id=id)\
                    .first()

                # get the message and tracking for order
                msg = db.session\
                    .query(shippingSecret)\
                    .filter_by(orderid=id)\
                    .first()
                gettracking = db.session\
                    .query(Tracking)\
                    .filter_by(sale_id=id)\
                    .first()
                if msg:
                    msg = msg
                else:
                    msg = 2
                return render_template('/vendor/vieworder.html',
                                       order=order,
                                       item=getitem,
                                       returninfo=returninfo,
                                       returntracking=returntracking,
                                       returns=returns,
                                       vendortracking=vendortracking,
                                       msg=msg,
                                       gettracking=gettracking,
                                       tracking=tracking
                                       )
        else:
            flash("Cannot view Order.", category="danger")
            return redirect(url_for('index'))
    else:
        flash("Order doesnt exist on clearnet_webapp.", category="danger")
        return redirect(url_for('index'))


@vendor.route('/vendor-refunds', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorRefunds():
    now = datetime.utcnow()

    user, \
        order, \
        issues, \
        getnotifications, \
        customerdisputes \
        = headerfunctions_vendor()

    # See if user has default return address
    try:
        getdefaultreturn = db.session\
            .query(DefaultReturns)\
            .filter_by(username=user.username)\
            .first()
        if getdefaultreturn:
            getdefaultreturn = 1
        else:
            getdefaultreturn = 0
    except Exception:
        getdefaultreturn = 0

    disputed = db.session\
        .query(Orders)\
        .filter(Orders.vendor == current_user.username, Orders.disputed_order == 1)\
        .all()

    returnorder = db.session\
        .query(Orders)\
        .filter(Orders.vendor == current_user.username, Orders.request_return.between(1, 3))\
        .all()

    return render_template('/vendor/vendorRefunds.html',
                           returnorder=returnorder,
                           getdefaultreturn=getdefaultreturn,
                           disputed=disputed,
                           now=now,
                           user=user,
                           order=order,
                           issues=issues,
                           getnotifications=getnotifications,
                           customerdisputes=customerdisputes
                           )


@vendor.route('/return-add-address/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def addtempaddress(id):
    now = datetime.utcnow()
    form = addtempreturn()
    order = db.session\
        .query(Orders)\
        .filter_by(id=id)\
        .first()

    # figure out price
    getitem = db.session\
        .query(marketItem)\
        .filter(marketItem.id == order.item_id)\
        .first()
    totalprice = (Decimal(order.shipping_price) + Decimal(order.price))

    msg = db.session\
        .query(shippingSecret)\
        .filter_by(orderid=id)\
        .first()
    gettracking = db.session\
        .query(Tracking)\
        .filter_by(sale_id=id)\
        .first()
    if request.method == 'POST' and form.validate_on_submit():
        if current_user.id == order.vendor_id:
            if order.released == 0 and order.completed == 0:
                if form.submit.data:
                    addtemp = Returns(
                        ordernumber=id,
                        name=form.name.data,
                        street=form.street.data,
                        city=form.city.data,
                        state=form.state.data,
                        country=form.country.data,
                        zip=form.zip.data,
                        message=form.messagereturn.data,
                    )
                    db.session.add(addtemp)
                    db.session.flush()

                    order.return_id = addtemp.id
                    order.request_return = 2
                    db.session.add(order)

                    db.session.commit()
                    flash("Return address added for Order#" + str(order.id),
                          category="success")
                    return redirect(url_for('vendor.vendorRefunds', username=current_user.username))

                elif form.cancelandrefund.data:

                    order.completed = 1
                    order.disputed_order = 0
                    order.new_order = 0
                    order.accepted_order = 0
                    order.waiting_order = 0
                    order.delivered_order = 1
                    order.request_cancel = 0
                    order.reason_cancel = 0
                    order.request_return = 0
                    order.released = 1
                    order.cancelled = 0
                    order.incart = 0
                    order.modid = 0
                    order.completed_time = now

                    db.session.add(order)

                    notification(type=111,
                                 username=order.customer,
                                 user_id=order.customer_id,
                                 salenumber=order.id,
                                 bitcoin=0)
                    notification(type=111, username=order.vendor,
                                 user_id=order.vendor_id,
                                 salenumber=order.id,
                                 bitcoin=0)

                    btc_cash_sendCointoclearnet(amount=order.fee,
                                                comment=order.id,
                                                shard=current_user.shard
                                                )
                    btc_cash_sendCointoUser(amount=totalprice,
                                            comment=order.id,
                                            user_id=order.vendor_id,
                                            )

                    # BTC CASH Spent by user
                    totalspentonitems_btccash(
                        user_id=order.customer_id, howmany=1, amount=order.price)

                    # BTC CASH recieved by vendor
                    vendortotalmade_btccash(
                        user_id=order.vendor_id, amount=order.price)

                    # Delete temp message vendor gave
                    if msg:
                        db.session.delete(msg)
                    if gettracking:
                        db.session.delete(gettracking)

                    # Add total items bought
                    addtotalItemsBought(
                        user_id=order.customer_id, howmany=order.quantity)

                    # add total sold to vendor
                    addtotalItemsSold(user_id=order.vendor_id,
                                      howmany=order.quantity)

                    # add diff trading partners
                    differenttradingpartners_user(
                        user_id=order.customer_id, otherid=order.vendor_id)
                    differenttradingpartners_vendor(
                        user_id=order.vendor_id, otherid=order.customer_id)

                    # customer exp for finishing early
                    exppoint(user=order.customer_id, price=0,
                             type=5, quantity=0, currency=0)

                    # Give Vendor experience points for sale
                    exppoint(user=order.vendor_id, price=order.price, type=10,
                             quantity=order.quantity, currency=order.currency)

                    # Give user experience points for sale
                    exppoint(user=order.customer_id, price=order.price, type=1,
                             quantity=order.quantity, currency=order.currency)

                    db.session.commit()
                    flash("Cancelled and refunded. Order#" +
                          str(order.id), category="success")
                    return redirect(url_for('vendor.vendorRefunds', username=current_user.username))
                else:
                    flash("Error", category="danger")
                    return redirect(url_for('index', username=current_user.username))
            else:
                flash("Error", category="danger")
                return redirect(url_for('index', username=current_user.username))
        else:
            flash("Error", category="danger")
            return redirect(url_for('index', username=current_user.username))
    return render_template('/vendor/vieworder.html',
                           form=form,
                           order=order,
                           msg=msg,
                           gettracking=gettracking,
                           item=getitem,
                           )


@vendor.route('/return-edit-address/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def edittempaddress(id):
    returnaddress = db.session\
        .query(Returns)\
        .filter_by(ordernumber=id)\
        .first()
    order = db.session\
        .query(Orders)\
        .filter_by(id=id)\
        .first()
    getitem = db.session\
        .query(marketItem)\
        .filter(marketItem.id == order.item_id)\
        .first()
    # vendor is True

    try:
        form = addtempreturn(
            ordernumber=returnaddress.id,
            name=returnaddress.name,
            street=returnaddress.street,
            city=returnaddress.city,
            state=returnaddress.state,
            country=returnaddress.country,
            zip=returnaddress.zip,
            messagereturn=returnaddress.message
        )
    except Exception:
        form = addtempreturn()

    if request.method == 'POST' and form.validate_on_submit():
        returnaddress.ordernumber = id,
        returnaddress.name = form.name.data,
        returnaddress.street = form.street.data,
        returnaddress.city = form.city.data,
        returnaddress.state = form.state.data,
        returnaddress.country = form.country.data,
        returnaddress.zip = form.zip.data,
        returnaddress.message = form.messagereturn.data,

        db.session.add(returnaddress)
        db.session.commit()
        flash("Return address added for Order#" +
              str(order.id), category="success")
        return redirect(url_for('vendor.vendorRefunds', username=current_user.username))

    return render_template('/vendor/vieworder.html',  form=form,
                           order=order,
                           vendor=vendor,
                           item=getitem,
                           returnaddress=returnaddress,
                           )


@vendor.route('/vendor-markasreturned/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorOrders_recievereturn(id):
    now = datetime.utcnow()
    # sent vendor order to recieved
    vendororder = db.session\
        .query(Orders)\
        .filter_by(id=id)\
        .first()
    msg = db.session\
        .query(shippingSecret)\
        .filter_by(orderid=id)\
        .first()
    gettracking = db.session\
        .query(Tracking)\
        .filter_by(sale_id=id)\
        .first()

    if vendororder.vendor_id == current_user.id and vendororder.released == 0:
        vendororder.request_return = 5
        vendororder.completed = 1
        vendororder.new_order = 0
        vendororder.released = 1
        vendororder.accepted_order = 0
        vendororder.waiting_order = 0
        vendororder.delivered_order = 0
        vendororder.completed_time = now

        db.session.add(vendororder)

        try:
            # Delete temp message vendor gave
            tempaddress = db.session\
                .query(Returns)\
                .filter_by(ordernumber=id)\
                .first()
            if tempaddress:
                db.session.delete(tempaddress)

            # Delete temp message vendor gave
            if msg:
                db.session.delete(msg)
            if gettracking:
                db.session.delete(gettracking)
        except:
            db.session.rollback()

        try:
            # delete return tracking number
            returntracking = db.session\
                .query(ReturnsTracking)\
                .filter_by(ordernumber=id)\
                .first()
            db.session.delete(returntracking)

        except:
            db.session.rollback()
        # give user bad exp

        exppoint(user=vendororder.customer_id, price=0,
                 type=10, quantity=0, currency=0)

        # calculate vendor amount
        pricewithoutshipping = Decimal(vendororder.price)
        shiprice = Decimal(vendororder.shipping_price)
        refundamount = Decimal(vendororder.return_amount)

        # he gets shipping + cost leftover after quant
        vendorgets = (pricewithoutshipping-refundamount) + shiprice
        comment = str(vendororder.id)

        # notify customer
        notification(type=8,
                     username=vendororder.customer,
                     user_id=vendororder.customer_id,
                     salenumber=vendororder.id,
                     bitcoin=vendororder.return_amount)
        # transfer money back to user from clearnet account
        # notify vendor
        notification(type=6,
                     username=vendororder.customer,
                     user_id=vendororder.customer_id,
                     salenumber=vendororder.id,
                     bitcoin=vendororder.return_amount
                     )
        # notify vendor
        notification(type=8,
                     username=vendororder.vendor,
                     user_id=vendororder.vendor_id,
                     salenumber=vendororder.id,
                     bitcoin=0
                     )

        btc_cash_sendCointoUser(amount=vendororder.return_amount,
                                comment=comment,
                                user_id=vendororder.vendor_id,
                                )

        if vendorgets > 0:

            btc_cash_sendCointoUser(amount=vendorgets,
                                    comment=comment,
                                    user_id=vendororder.vendor_id,
                                    )

        try:
            # delete return address
            returninfo = db.session\
                .query(Returns)\
                .filter_by(ordernumber=id)\
                .first()
            if returninfo:
                db.session.delete(returninfo)
        except Exception:
            pass
        try:
            # delete return tracking
            returntracking = db.session\
                .query(ReturnsTracking)\
                .filter_by(ordernumber=id)\
                .first()
            if returntracking:
                db.session.delete(returntracking)
        except Exception:
            pass
        db.session.commit()
        flash("Order Marked as returned", category="success")
        return redirect(url_for('vendor.vendorOrders', username=current_user.username))
    else:
        return redirect(url_for('index'))


@vendor.route('/vendor-orders', methods=['GET'])
@website_offline
@login_required
@vendoraccount_required
def vendorOrders():
    now = datetime.utcnow()
    user, \
        order, \
        issues, \
        getnotifications, \
        customerdisputes \
        = headerfunctions_vendor()
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args()
    # PEr Page tells how many search results pages
    inner_window = 5  # search bar at bottom used for .. lots of pages
    outer_window = 5  # search bar at bottom used for .. lots of pages
    per_page = 10

    ordernew_overall = db.session\
        .query(Orders)\
        .filter(Orders.vendor_id == user.id,
                Orders.new_order == 1,
                Orders.completed == 0,
                Orders.type == 1
                )\
        .order_by(Orders.id.desc())
    ordernew = ordernew_overall.limit(per_page).offset(offset)
    ordernewcount = ordernew_overall.count()
    paginationordernew = Pagination(page=page,
                                    total=ordernew_overall.count(),
                                    search=search,
                                    record_name='items',
                                    offset=offset,
                                    per_page=per_page,
                                    css_framework='bootstrap5',
                                    inner_window=inner_window,
                                    outer_window=outer_window)

    orderaccepted1 = db.session\
        .query(Orders)\
        .filter(Orders.vendor_id == user.id,
                Orders.accepted_order == 1,
                Orders.completed == 0,
                Orders.type == 1
                )

    orderaccepted1 = orderaccepted1.order_by(Orders.id.desc())
    orderaccepted = orderaccepted1.limit(per_page).offset(offset)
    orderacceptedcount = orderaccepted1.count()
    paginationorderaccepted = Pagination(page=page,
                                         total=orderaccepted1.count(),
                                         search=search,
                                         record_name='items',
                                         offset=offset,
                                         per_page=per_page,
                                         css_framework='bootstrap4',
                                         inner_window=inner_window,
                                         outer_window=outer_window)

    orderwaiting1 = db.session\
        .query(Orders)\
        .filter(Orders.vendor_id == user.id,
                Orders.waiting_order == 1,
                Orders.completed == 0,
                Orders.type == 1
                )
    orderwaiting1 = orderwaiting1.order_by(Orders.id.desc())
    orderwaiting = orderwaiting1.limit(per_page).offset(offset)
    orderwaitingcount = orderwaiting1.count()
    paginationorderwaiting = Pagination(page=page,
                                        total=orderwaiting1.count(),
                                        search=search,
                                        record_name='items',
                                        offset=offset,
                                        per_page=per_page,
                                        css_framework='bootstrap5',
                                        inner_window=inner_window,
                                        outer_window=outer_window)

    completed1 = db.session\
        .query(Orders)\
        .filter(Orders.vendor_id == user.id,
                Orders.completed == 1,
                Orders.type == 1
                )
    completed1 = completed1.order_by(Orders.id.desc())
    completed = completed1.limit(per_page).offset(offset)
    completedcount = completed1.count()
    paginationcompleted = Pagination(page=page,
                                     total=completed1.count(),
                                     search=search,
                                     record_name='items',
                                     offset=offset,
                                     per_page=per_page,
                                     css_framework='bootstrap5',
                                     inner_window=inner_window,
                                     outer_window=outer_window)

    return render_template('/vendor/vendorOrders.html',
                           user=user, now=now,
                           completed=completed,
                           ordernew=ordernew,
                           orderaccepted=orderaccepted,
                           orderwaiting=orderwaiting,
                           ordernewcount=ordernewcount,
                           orderacceptedcount=orderacceptedcount,
                           orderwaitingcount=orderwaitingcount,
                           completedcount=completedcount,
                           paginationordernew=paginationordernew,
                           paginationorderaccepted=paginationorderaccepted,
                           paginationorderwaiting=paginationorderwaiting,
                           paginationcompleted=paginationcompleted,
                           order=order,
                           issues=issues,
                           getnotifications=getnotifications,
                           customerdisputes=customerdisputes
                           )


@vendor.route('/becomeverified', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorverification():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()

    seeifvendoropenorder = db.session\
        .query(Orders)\
        .filter(Orders.released == 0, Orders.completed == 0)\
        .first()

    if seeifvendoropenorder is None:
        allow = 1
    else:
        allow = 0
    hundred = btc_cash_convertlocaltobtc(amount=100, currency=0)
    twofity = btc_cash_convertlocaltobtc(amount=250, currency=0)
    fivehundred = btc_cash_convertlocaltobtc(amount=500, currency=0)
    thousand = btc_cash_convertlocaltobtc(amount=1000, currency=0)
    twentyfivehundred = btc_cash_convertlocaltobtc(amount=2500, currency=0)

    if request.method == 'POST':
        if form.cancel.data:
            if allow == 1:

                return redirect(url_for('vendor.vendorverificationcancel'))
            else:
                flash("Cannot Cancel yur verification", category="danger")
        if getverify.vendor_level == 0:
            if form.levelzero.data:
                flash(
                    "You can become verified at a later time. Its optional..", category="success")
                return redirect(url_for('vendor.tradeOptions'))
            elif form.levelone.data:
                return redirect(url_for('vendor.vendorverification_confirm_level1'))
            elif form.leveltwo.data:
                return redirect(url_for('vendor.vendorverification_confirm_level2'))
            elif form.levelthree.data:
                return redirect(url_for('vendor.vendorverification_confirm_level3'))
            elif form.levelfour.data:
                return redirect(url_for('vendor.vendorverification_confirm_level4'))
            elif form.levelfive.data:
                return redirect(url_for('vendor.vendorverification_confirm_level5'))
            else:
                pass
        else:
            return redirect(url_for('vendor.upgradevendorverification'))

    return render_template('/vendor/verification/verification.html',
                           form=form,
                           user=user,
                           allow=allow,
                           getverify=getverify,
                           now=now,
                           hundred=hundred,
                           twofity=twofity,
                           fivehundred=fivehundred,
                           thousand=thousand,
                           twentyfivehundred=twentyfivehundred,
                           )


@vendor.route('/cancelverified', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorverificationcancel():
    now = datetime.utcnow()
    form = ConfirmCancel()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()
    user1getlevel = db.session\
        .query(UserAchievements)\
        .filter_by(username=user.username)\
        .first()
    user1pictureid = str(user1getlevel.level)
    seeifvendoropenorder = db.session\
        .query(Orders)\
        .filter(Orders.released == 0, Orders.completed == 0)\
        .first()
    if seeifvendoropenorder is None:
        allow = 1
    else:
        allow = 0
    hundred = btc_cash_convertlocaltobtc(amount=100, currency=0)
    twofity = btc_cash_convertlocaltobtc(amount=250, currency=0)
    fivehundred = btc_cash_convertlocaltobtc(amount=500, currency=0)
    thousand = btc_cash_convertlocaltobtc(amount=1000, currency=0)
    twentyfivehundred = btc_cash_convertlocaltobtc(amount=2500, currency=0)

    if request.method == 'POST':
        if getverify.vendor_level != 0:
            if form.confirmcancel.data:
                if allow == 1:
                    btc_cash_sendCoinfromHoldings(amount=getverify.amount,
                                                  user_id=getverify.vendor_id,
                                                  comment=getverify.vendor_level
                                                  )
                    getverify.vendor_level = 0
                    getverify.timestamp = now
                    getverify.amount = 0
                    db.session.add(getverify)
                    db.session.commit()

                    flash("Trust level removed, account refunded",
                          category="success")
                    return redirect(url_for('vendor.tradeOptions'))
                else:
                    flash("Cannot Cancel yur verification", category="danger")
                    return redirect(url_for('vendor.vendorverification'))
            else:
                return redirect(url_for('vendor.vendorverification'))
        else:
            return redirect(url_for('vendor.vendorverification'))

    return render_template('/vendor/verification/confirmcancel.html',
                           form=form,
                           user=user,
                           allow=allow,
                           getverify=getverify,
                           now=now,
                           hundred=hundred,
                           twofity=twofity,
                           fivehundred=fivehundred,
                           thousand=thousand,
                           twentyfivehundred=twentyfivehundred,
                           user1pictureid=user1pictureid
                           )


@vendor.route('/becomeverified-level1', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorverification_confirm_level1():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()

    if user.vendor_account == 1 and getverify.vendor_level == 0:
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()
        useramount = userwallet.currentbalance

        hundred = btc_cash_convertlocaltobtc(amount=100, currency=0)
        Decimalhundred = Decimal(hundred)

        if request.method == 'POST':
            if form.levelone.data:
                # 100 dollars
                if useramount > Decimalhundred:
                    btc_cash_sendCointoHoldings(
                        amount=hundred, user_id=current_user.id, comment=1)
                    getverify.vendor_level = 1
                    getverify.timestamp = now
                    getverify.amount = Decimalhundred
                    db.session.add(getverify)

                    obtainedtrustlevel(user_id=user.id)

                    db.session.commit()
                    flash("You are now a trust level 1 vendor. "
                          "The BTC has been deducted from your account", category="success")
                    return redirect(url_for('vendor.tradeOptions'))
                else:
                    # user doesnt have 100$
                    flash(
                        "You do not have enough bitcoin in your wallet_btc.", category="danger")
                    return redirect(url_for('vendor.vendorverification'))
            else:
                flash(
                    "You can become verified at a later time. Its optional..", category="success")
                return redirect(url_for('vendor.tradeOptions'))

        return render_template('/vendor/verification/confirmverification_level1.html',
                               form=form,
                               user=user,
                               getverify=getverify,
                               now=now,
                               hundred=hundred,
                               )
    else:
        flash("Not a vendor", category="danger")
        return redirect(url_for('index'))


@vendor.route('/becomeverified-level2', methods=['GET', 'POST'])
@website_offline
@login_required
@ping_user
@vendoraccount_required
def vendorverification_confirm_level2():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()
    if user.vendor_account == 1 and getverify.vendor_level == 0:
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()

        useramount = userwallet.currentbalance

        twofity = btc_cash_convertlocaltobtc(amount=250, currency=0)
        Decimaltwofity = Decimal(twofity)

        if request.method == 'POST':
            if form.leveltwo.data:
                if useramount > Decimaltwofity:
                    # 250 dollars
                    btc_cash_sendCointoHoldings(
                        amount=twofity, user_id=current_user.id, comment=2)
                    getverify.vendor_level = 2
                    getverify.timestamp = now
                    getverify.amount = Decimaltwofity
                    db.session.add(getverify)

                    obtainedtrustlevel(user_id=user.id)

                    db.session.commit()
                    flash("You are now a trust level 2 vendor. "
                          "The BTC has been deducted from your account", category="success")
                    return redirect(url_for('vendor.tradeOptions'))
                else:
                    # user doesnt have 250$
                    flash(
                        "You do not have enough bitcoin in your wallet_btc.", category="danger")
                    return redirect(url_for('vendor.vendorverification'))
            else:
                flash(
                    "You can become verified at a later time. Its optional..", category="success")
                return redirect(url_for('vendor.tradeOptions'))

        return render_template('/vendor/verification/confirmverification_level2.html',
                               form=form,
                               user=user,
                               getverify=getverify,
                               now=now,
                               twofity=twofity,
                               )
    else:
        flash("Not a vendor", category="danger")
        return redirect(url_for('index'))


@vendor.route('/becomeverified-level3', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorverification_confirm_level3():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()

    if user.vendor_account == 1 and getverify.vendor_level == 0:
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()
        useramount = userwallet.currentbalance

        fivehundred = btc_cash_convertlocaltobtc(amount=500, currency=0)
        Decimalfivehundred = Decimal(fivehundred)

        if request.method == 'POST':
            if form.levelthree.data:
                if useramount > Decimalfivehundred:
                    btc_cash_sendCointoHoldings(
                        amount=fivehundred, user_id=current_user.id, comment=3)
                    getverify.vendor_level = 3
                    getverify.timestamp = now
                    getverify.amount = Decimalfivehundred
                    db.session.add(getverify)

                    obtainedtrustlevel(user_id=user.id)

                    db.session.commit()
                    flash("You are now a trust level 3 vendor. "
                          "The BTC has been deducted from your account",
                          category="success")
                    return redirect(url_for('vendor.tradeOptions'))
                else:
                    # user doesnt have 500$
                    flash(
                        "You do not have enough bitcoin in your wallet_btc.", category="danger")
                    return redirect(url_for('vendor.vendorverification'))
            else:
                flash(
                    "You can become verified at a later time. Its optional..", category="success")
                return redirect(url_for('vendor.tradeOptions'))

        return render_template('/vendor/verification/confirmverification_level3.html',
                               form=form,
                               user=user,
                               getverify=getverify,
                               now=now,
                               fivehundred=fivehundred,
                               )
    else:
        flash("Not a vendor", category="danger")
        return redirect(url_for('index'))


@vendor.route('/becomeverified-level4', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorverification_confirm_level4():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()
    if user.vendor_account == 1 and getverify.vendor_level == 0:
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()
        useramount = userwallet.currentbalance

        thousand = btc_cash_convertlocaltobtc(amount=1000, currency=0)
        Decimalthousand = Decimal(thousand)

        if request.method == 'POST':
            if useramount > Decimalthousand:
                btc_cash_sendCointoHoldings(
                    amount=thousand, user_id=current_user.id, comment=4)
                getverify.vendor_level = 4
                getverify.timestamp = now
                getverify.amount = Decimalthousand
                db.session.add(getverify)

                obtainedtrustlevel(user_id=user.id)

                db.session.commit()
                flash("You are now a trust level 4 vendor."
                      " The BTC has been deducted from your account",
                      category="success")
                return redirect(url_for('vendor.tradeOptions'))
            else:
                # user doesnt have 1000$
                flash("You do not have enough bitcoin in your wallet_btc.",
                      category="danger")
                return redirect(url_for('vendor.vendorverification'))

        return render_template('/vendor/verification/confirmverification_level4.html',
                               form=form,
                               user=user,
                               getverify=getverify,
                               now=now,
                               thousand=thousand,
                               )
    else:
        flash("Not a vendor", category="danger")
        return redirect(url_for('index'))


@vendor.route('/becomeverified-level5', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorverification_confirm_level5():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()
    if user.vendor_account == 1 and getverify.vendor_level == 0:
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()
        useramount = userwallet.currentbalance

        twentyfivehundred = btc_cash_convertlocaltobtc(amount=2500, currency=0)
        Decimaltwentyfivehundred = Decimal(twentyfivehundred)

        if request.method == 'POST':
            if form.levelfive.data:
                if useramount > Decimaltwentyfivehundred:
                    btc_cash_sendCointoHoldings(
                        amount=twentyfivehundred, user_id=current_user.id, comment=5)
                    getverify.vendor_level = 5
                    getverify.timestamp = now
                    getverify.amount = Decimaltwentyfivehundred
                    db.session.add(getverify)

                    obtainedtrustlevel(user_id=user.id)

                    db.session.commit()
                    flash("You are now a trust level 5 vendor. "
                          "The BTC has been deducted from your account",
                          category="success")
                    return redirect(url_for('vendor.tradeOptions'))
                else:
                    # user doesnt have 2500$
                    flash(
                        "You do not have enough bitcoin in your wallet_btc.", category="danger")
                    return redirect(url_for('vendor.vendorverification'))
            else:
                flash(
                    "You can become verified at a later time. Its optional..", category="success")
                return redirect(url_for('vendor.tradeOptions'))

        return render_template('/vendor/verification/confirmverification_level5.html',
                               form=form,
                               user=user,
                               getverify=getverify,
                               now=now,
                               twentyfivehundred=twentyfivehundred,
                               )

    else:
        flash("Not a vendor", category="danger")
        return redirect(url_for('index'))


@vendor.route('/upgradeverified', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def upgradevendorverification():
    now = datetime.utcnow()
    form = vendorVerify()
    getverify = db.session\
        .query(vendorVerification)\
        .filter_by(vendor_id=current_user.id)\
        .first()
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()

    userwallet = db.session\
        .query(BchWallet)\
        .filter_by(user_id=current_user.id)\
        .first()
    useramount = userwallet.currentbalance

    twofity = btc_cash_convertlocaltobtc(amount=250, currency=0)
    fivehundred = btc_cash_convertlocaltobtc(amount=500, currency=0)
    thousand = btc_cash_convertlocaltobtc(amount=1000, currency=0)
    twentyfivehundred = btc_cash_convertlocaltobtc(amount=2500, currency=0)

    Decimaltwofity = Decimal(twofity)
    Decimalfivehundred = Decimal(fivehundred)
    Decimalthousand = Decimal(thousand)
    Decimaltwentyfivehundred = Decimal(twentyfivehundred)

    if request.method == 'POST':
        if current_user.id == getverify.vendor_id:
            # return refund
            # get new badge
            if form.leveltwo.data:
                if getverify.vendor_level == 1:
                    if useramount > Decimaltwofity:
                        btc_cash_sendCoinfromHoldings(
                            amount=getverify.amount, user_id=getverify.vendor_id, comment=getverify.vendor_level)
                        btc_cash_sendCointoHoldings(
                            amount=twofity, user_id=current_user.id, comment=2)
                        getverify.vendor_level = 2
                        getverify.timestamp = now
                        getverify.amount = Decimaltwofity
                        db.session.add(getverify)

                        db.session.commit()

                        flash("You are now a trust level 2 vendor. "
                              "The BTC has been deducted from your account",
                              category="success")
                        return redirect(url_for('vendor.tradeOptions'))
                    else:
                        # user doesnt have 250$
                        flash(
                            "You do not have enough bitcoin in your wallet_btc.", category="danger")
                        return redirect(url_for('vendor.vendorverification'))

            elif form.levelthree.data:
                if getverify.vendor_level == 1 \
                        or getverify.vendor_level == 2:
                    if useramount > Decimalfivehundred:
                        btc_cash_sendCoinfromHoldings(amount=getverify.amount, user_id=getverify.vendor_id,
                                                      comment=getverify.vendor_level)
                        btc_cash_sendCointoHoldings(
                            amount=fivehundred, user_id=current_user.id, comment=3)
                        getverify.vendor_level = 3
                        getverify.timestamp = now
                        getverify.amount = Decimalfivehundred
                        db.session.add(getverify)

                        db.session.commit()

                        flash("You are now a trust level 3 vendor. "
                              "The BTC has been deducted from your account",
                              category="success")
                        return redirect(url_for('vendor.tradeOptions'))
                    else:
                        # user doesnt have 500$
                        flash(
                            "You do not have enough bitcoin in your wallet_btc.", category="danger")
                        return redirect(url_for('vendor.vendorverification'))

            elif form.levelfour.data:
                if getverify.vendor_level == 1 \
                        or getverify.vendor_level == 2 \
                        or getverify.vendor_level == 3:
                    if useramount > Decimalthousand:
                        btc_cash_sendCoinfromHoldings(
                            amount=getverify.amount, user_id=getverify.vendor_id, comment=getverify.vendor_level)
                        btc_cash_sendCointoHoldings(
                            amount=thousand, user_id=current_user.id, comment=4)

                        getverify.vendor_level = 4
                        getverify.timestamp = now
                        getverify.amount = Decimalthousand
                        db.session.add(getverify)
                        db.session.commit()

                        flash("You are now a trust level 4 vendor."
                              " The BTC has been deducted from your account",
                              category="success")
                        return redirect(url_for('vendor.tradeOptions'))
                    else:
                        # user doesnt have 1000$
                        flash(
                            "You do not have enough bitcoin in your wallet_btc.", category="danger")
                        return redirect(url_for('vendor.vendorverification'))
            elif form.levelfive.data:
                if getverify.vendor_level == 1 \
                        or getverify.vendor_level == 2 \
                        or getverify.vendor_level == 3 \
                        or getverify.vendor_level == 4:
                    if useramount > Decimaltwentyfivehundred:
                        btc_cash_sendCoinfromHoldings(
                            amount=getverify.amount, user_id=getverify.vendor_id, comment=getverify.vendor_level)
                        btc_cash_sendCointoHoldings(
                            amount=twentyfivehundred, user_id=current_user.id, comment=5)

                        getverify.vendor_level = 5
                        getverify.timestamp = now
                        getverify.amount = Decimaltwentyfivehundred
                        db.session.add(getverify)
                        db.session.commit()

                        flash("You are now a trust level 5 vendor."
                              " The BTC has been deducted from your account",
                              category="success")
                        return redirect(url_for('vendor.tradeOptions'))
                    else:
                        # user doesnt have $
                        flash(
                            "You do not have enough bitcoin in your wallet_btc.", category="danger")
                        return redirect(url_for('vendor.vendorverification'))
            else:
                flash("Form Error", category="danger")
                return redirect(url_for('vendor.vendorverification'))
        else:
            flash("Form Error", category="danger")
            return redirect(url_for('vendor.vendorverification'))
    return render_template('/vendor/verification/upgradeverification.html',
                           form=form,
                           user=user,
                           getverify=getverify,
                           now=now,
                           twofity=twofity,
                           fivehundred=fivehundred,
                           thousand=thousand,
                           twentyfivehundred=twentyfivehundred,
                           )


@vendor.route('/itemimporter', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def ebayimporter():
    # variables
    now = datetime.utcnow()
    id_pic1 = id_generator_picture1()

    # forms
    form = UploadEbayForm()

    # queries
    user = db.session\
        .query(User)\
        .filter_by(id=current_user.id)\
        .first()
    getalluploads = db.session\
        .query(EbaySearchItem)\
        .filter_by(user_id=current_user.id)\
        .order_by(EbaySearchItem.dateadded.desc())\
        .limit(100)
    getalluploadscount = db.session\
        .query(EbaySearchItem)\
        .filter_by(user_id=current_user.id)\
        .count()

    if request.method == 'POST':
        if form.submit.data:
            if form.validate():
                if form.ebaydata.data:
                    directoryifitemlisting = os.path.join(
                        UPLOADED_FILES_DEST, "ebaywork", (str(user.id)))
                    mkdir_p(path=directoryifitemlisting)
                    filename = secure_filename(form.ebaydata.data.filename)
                    # makes directory (generic location + auction number id as folder)
                    # saves it to location
                    csvpath = os.path.join(directoryifitemlisting, filename)
                    form.ebaydata.data.save(csvpath)
                    # split file name and ending
                    filenamenew, file_extension = os.path.splitext(csvpath)
                    # gets new 64 digit filenam
                    newfileName = id_pic1 + file_extension
                    # puts new name with ending
                    filenamenewfull = filenamenew + file_extension
                    # gets aboslute path of new file
                    newfileNameDestination = os.path.join(
                        directoryifitemlisting, newfileName)
                    # renames file
                    os.rename(filenamenewfull, newfileNameDestination)
                    if form.ebaydata.data.filename:
                        with open(newfileNameDestination) as csvfile:
                            readCSV = csv.reader(csvfile, delimiter=',')
                            next(readCSV, None)
                            for row in readCSV:

                                ebaytitle = (row[0])
                                ebayitemid = (row[1])
                                quantity = (row[2])
                                fixedprice = (row[5])
                                condition = (row[8])
                                category = (row[12])

                                if len(fixedprice) > 1:
                                    dollars_dec = Decimal(
                                        fixedprice.strip('$'))
                                else:
                                    dollars_dec = 0

                                if 'Good' in condition:
                                    protoscondition = 4
                                elif 'used' in condition:
                                    protoscondition = 4
                                elif 'parts' in condition:
                                    protoscondition = 5
                                elif 'seller' in condition:
                                    protoscondition = 3
                                elif 'Manufacturer' in condition:
                                    protoscondition = 2
                                elif 'New' in condition:
                                    protoscondition = 1
                                else:
                                    protoscondition = 6

                                newitem = EbaySearchItem(
                                    dateadded=now,
                                    user_id=current_user.id,
                                    itemebayid=ebayitemid,
                                    itemtitle=ebaytitle,
                                    itemprice=dollars_dec,
                                    itemquantity=quantity,
                                    itemcondition=protoscondition,
                                    itemcategory=category,
                                    status=0,
                                )

                                db.session.add(newitem)

                            db.session.commit()
                            flash("Your auctions will be added within an hour.  If there are any issues,"
                                  "please report them to customer feedback.", category="success")
                            return redirect(url_for('vendor.ebayimporter'))
                    else:
                        flash("Form Error. Only CSV's allowed.",
                              category="danger")
                        return redirect(url_for('vendor.ebayimporter'))
                else:
                    flash("Form Error. Only CSV's allowed.", category="danger")
                    return redirect(url_for('vendor.ebayimporter'))
            else:
                flash("Form Error. Only CSV's allowed.", category="danger")
                return redirect(url_for('vendor.ebayimporter'))
        elif form.delete.data:
            for f in getalluploads:
                if f.user_id == current_user.id:
                    db.session.delete(f)
            db.session.commit()
            flash("Items deleted ", category="danger")
            return redirect(url_for('vendor.ebayimporter'))
        else:
            flash("Form Error. Only CSV's allowed.", category="danger")
            return redirect(url_for('vendor.ebayimporter'))

    return render_template('/vendor/tools/ebayimporter.html',
                           form=form,
                           user=user,
                           now=now,
                           getalluploads=getalluploads,
                           getalluploadscount=getalluploadscount
                           )
