from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.vendorcreate import vendorcreate
import shutil
import os
from app import UPLOADED_FILES_DEST, UPLOADED_FILES_DEST_ITEM
from werkzeug.datastructures import CombinedMultiDict
from decimal import Decimal
from app.search.searchfunction import headerfunctions_vendor
from flask_paginate import Pagination, get_page_args
from app.common.decorators import \
    website_offline, \
    login_required, \
    ping_user, \
    vendoraccount_required
from app.common.functions import \
    mkdir_p, \
    itemlocation
from app.common.functions import \
    mkdir_p, \
    id_generator_picture1
# forms
from app.vendorcreate.forms import add_product_form_factory

# forms
from app.vendorcreate.forms import \
    deactive, \
    UploadEbayForm
# models
from app.classes.auth import User

from app.classes.item import \
    marketItem
from app.classes.vendor import \
    EbaySearchItem

from app.classes.wallet_bch import *
from app.vendor.images.image_forms import image1, image2, image3, image4, image5


@vendorcreate.route('/trade-options/')
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


@vendorcreate.route('/myitems', methods=['GET', 'POST'])
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
    sale = db.session.query(marketItem).filter(marketItem.vendor_id == user.id).order_by(
        marketItem.totalsold.desc(), marketItem.online.desc(), marketItem.id.desc())

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
                            flash(
                                f"Item #{str(specific_item.id)} Doesnt have very good keywords", category="warning")
                            see_if_changes.append(1)
                        # Turn off
                        if len(specific_item.imageone) < 10:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash(
                                f"Item# {str(specific_item.id)} Doesnt have a main image. Cannot put item online.", category="danger")
                            see_if_changes.append(1)

                        if specific_item.destinationcountry == '0':
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash(
                                f"Item #{str(specific_item.id)} Doesnt have a destination country. Cannot put item online.", category="danger")
                            see_if_changes.append(1)

                        if specific_item.origincountry == '0':
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash(
                                f"Item #{str(specific_item.id)} Doesnt have an origin. Cannot put item online.", category="danger")
                            see_if_changes.append(1)

                        if specific_item.itemcount <= 0:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash(
                                f"Item #{str(specific_item.id)} Has been Sold out.  Update quantity to re-list it. Cannot put item online.",  category="danger")
                            see_if_changes.append(1)

                        # needs price
                        if Decimal(specific_item.price) < .000001:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash(
                                f"Item #{str(specific_item.id)} Doesnt have a proper price. Cannot put item online.", category="danger")
                            see_if_changes.append(1)

                        if len(specific_item.itemtitlee) < 10:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash(
                                f"Item# {str(specific_item.id)} Doesnt have a proper title. Cannot put item online.", category="danger")
                            see_if_changes.append(1)

                        if specific_item.shippingtwo == 1:
                            if Decimal(specific_item.shippingprice2) > .01:
                                if len(specific_item.shippinginfo2) >= 2:
                                    pass
                            else:
                                specific_item.shippingtwo = 0
                                db.session.add(specific_item)
                                flash(
                                    f"Item# + {str(specific_item.id)} Doesnt have a proper shipping price 2.", category="danger")
                                see_if_changes.append(1)

                        if specific_item.shippingthree == 1:
                            if Decimal(specific_item.shippingprice3) > .01:
                                if len(specific_item.shippinginfo3) >= 2:
                                    pass
                            else:
                                specific_item.shippingthree = 0
                                db.session.add(specific_item)
                                flash(
                                    f"Item #{str(specific_item.id)} Doesnt have a proper shipping info 3 or price.", category="danger")
                                see_if_changes.append(1)

                        if specific_item.shippingfree == 0 \
                                and specific_item.shippingtwo == 0 \
                                and specific_item.shippingthree == 0:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash(
                                f"Item #{str(specific_item.id)} Doesnt have a shipping method selected/checked. Cannot put item online.", category="danger")
                            see_if_changes.append(1)

                except Exception as e:
                    print(str(e))
                    flash(
                        "Error!  There was an error putting the listings on/offline", category="danger")
                    specific_item.online = 0
                    db.session.add(specific_item)
                    db.session.commit()

            if len(see_if_changes) > 0:
                db.session.commit()
        else:
            flash(
                "You are currently on vacation mode.  Cannot put items online", category="danger")

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


@vendorcreate.route('/itemimporter', methods=['GET', 'POST'])
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
                            return redirect(url_for('vendorcreate.ebayimporter'))
                    else:
                        flash("Form Error. Only CSV's allowed.",
                              category="danger")
                        return redirect(url_for('vendorcreate.ebayimporter'))
                else:
                    flash("Form Error. Only CSV's allowed.", category="danger")
                    return redirect(url_for('vendorcreate.ebayimporter'))
            else:
                flash("Form Error. Only CSV's allowed.", category="danger")
                return redirect(url_for('vendorcreate.ebayimporter'))
        elif form.delete.data:
            for f in getalluploads:
                if f.user_id == current_user.id:
                    db.session.delete(f)
            db.session.commit()
            flash("Items deleted ", category="danger")
            return redirect(url_for('vendorcreate.ebayimporter'))
        else:
            flash("Form Error. Only CSV's allowed.", category="danger")
            return redirect(url_for('vendorcreate.ebayimporter'))

    return render_template('/vendor/tools/ebayimporter.html',
                           form=form,
                           user=user,
                           now=now,
                           getalluploads=getalluploads,
                           getalluploadscount=getalluploadscount
                           )


@vendorcreate.route('/create-an-item', methods=['GET', 'POST'])
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
    gettotalitems = db.session.query(marketItem).filter_by(
        vendor_id=current_user.id).count()
    if gettotalitems < 100:
        # item = 0 creating item       item = 1 editing item
        vendorcreateItem = add_product_form_factory(item=0)
        form = vendorcreateItem(CombinedMultiDict(
            (request.files, request.form)))

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
                directoryifitemlisting = os.path.join(
                    UPLOADED_FILES_DEST_ITEM, getimagesubfolder, (str(item.id)))
                mkdir_p(path=directoryifitemlisting)

                image1(formdata=form.imageone1.data, item=item,
                       directoryifitemlisting=directoryifitemlisting)
                image2(formdata=form.imagetwo.data, item=item,
                       directoryifitemlisting=directoryifitemlisting)
                image3(formdata=form.imagethree.data, item=item,
                       directoryifitemlisting=directoryifitemlisting)
                image4(formdata=form.imagefour.data, item=item,
                       directoryifitemlisting=directoryifitemlisting)
                image5(formdata=form.imagefive.data, item=item,
                       directoryifitemlisting=directoryifitemlisting)

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
                return redirect(url_for('vendorcreate.itemsforSale', username=current_user.username))

            return redirect(url_for('vendorcreate.createItem', username=current_user.username))

        return render_template('/vendor/itemsforsale/createItem.html',
                               form=form,
                               user=user)
    else:
        flash("100 items max", category="danger")
        return redirect(url_for('vendorcreate.itemsforSale', username=current_user.username))


@vendorcreate.route('/vendor-edititem/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def edititem(id):
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
                shippingthree=item.shippingthree,
                shippingtwo=item.shippingtwo,
                amazonid=0,
                amazon_last_checked=now,
            )

            if request.method == 'POST' and user.vendor_account == 1 and form.validate_on_submit():

                if item.vendor_id == user.id:
                    # Image location
                    getimagesubfolder = itemlocation(x=item.id)
                    directoryifitemlisting = os.path.join(
                        UPLOADED_FILES_DEST_ITEM, getimagesubfolder, (str(item.id)))
                    mkdir_p(path=directoryifitemlisting)

                    image1(formdata=form.imageone1.data, item=item,
                           directoryifitemlisting=directoryifitemlisting)
                    image2(formdata=form.imagetwo.data, item=item,
                           directoryifitemlisting=directoryifitemlisting)
                    image3(formdata=form.imagethree.data, item=item,
                           directoryifitemlisting=directoryifitemlisting)
                    image4(formdata=form.imagefour.data, item=item,
                           directoryifitemlisting=directoryifitemlisting)
                    image5(formdata=form.imagefive.data, item=item,
                           directoryifitemlisting=directoryifitemlisting)

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
                    cat0 = categoryfull.cat_id
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
                    getnotship4full = form.notshipping41.data
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

                    # Form data
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

                    flash(f"Updated: Item #{str(item.id)}",
                          category="success")
                    return redirect(url_for('vendorcreate.itemsforSale'))

            return render_template('/vendor/itemsforsale/edititem.html',
                                   form=form,
                                   item=item,
                                   user=user
                                   )
        else:
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@vendorcreate.route('/deletevendoritem/<int:id>', methods=['GET', 'POST'])
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
    ext_1 = '_225x'
    ext_2 = '_500x'
    item = marketItem.query.get(id)
    if item:
        if item.vendor_id == current_user.id:
            try:
                specific_folder = str(item.id)
                getitemlocation = itemlocation(x=item.id)
                link = 'item'

                pathtofile1 = os.path.join(
                    UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, item.imageone)
                pathtofile2 = os.path.join(
                    UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, item.imagetwo)
                pathtofile3 = os.path.join(
                    UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, item.imagethree)
                pathtofile4 = os.path.join(
                    UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, item.imagefour)
                pathtofile5 = os.path.join(
                    UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, item.imagefive)

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
                    pathtofile4, file_extension4 = os.path.splitext(
                        pathtofile4)
                except:
                    pass

                try:
                    pathtofile5, file_extension5 = os.path.splitext(
                        pathtofile5)
                except:
                    pass

                try:
                    delete_file_one = str(pathtofile1 + file_extension1)
                    delete_file_one_ext1 = str(
                        pathtofile1 + ext_1 + file_extension1)
                    delete_file_one_ext2 = str(
                        pathtofile1 + ext_2 + file_extension1)
                except:
                    pass

                try:
                    delete_file_two = str(pathtofile2 + file_extension2)
                    delete_file_two_ext1 = str(
                        pathtofile2 + ext_1 + file_extension2)
                    delete_file_two_ext2 = str(
                        pathtofile2 + ext_2 + file_extension2)
                except:
                    pass

                try:
                    delete_file_three = str(pathtofile3 + file_extension3)
                    delete_file_three_ext1 = str(
                        pathtofile3 + ext_1 + file_extension3)
                    delete_file_three_ext2 = str(
                        pathtofile3 + ext_2 + file_extension3)
                except:
                    pass

                try:
                    delete_file_four = str(pathtofile4 + file_extension4)
                    delete_file_four_ext1 = str(
                        pathtofile4 + ext_1 + file_extension4)
                    delete_file_four_ext2 = str(
                        pathtofile4 + ext_2 + file_extension4)
                except:
                    pass

                try:
                    delete_file_five = str(pathtofile5 + file_extension5)
                    delete_file_five_ext1 = str(
                        pathtofile5 + ext_1 + file_extension5)
                    delete_file_five_ext2 = str(
                        pathtofile5 + ext_2 + file_extension5)
                except:
                    pass

                item_one_image = item.imageone
                if len(item_one_image) > 10:
                    try:
                        os.remove(delete_file_one)
                    except:
                        pass
                    try:
                        os.remove(delete_file_one_ext1)
                        os.remove(delete_file_one_ext2)
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
                        os.remove(delete_file_two_ext1)
                        os.remove(delete_file_two_ext2)
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
                        os.remove(delete_file_three_ext1)
                        os.remove(delete_file_three_ext2)
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
                        os.remove(delete_file_four_ext1)
                        os.remove(delete_file_four_ext2)
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
                        os.remove(delete_file_five_ext1)
                        os.remove(delete_file_five_ext2)
                    except:
                        pass
                else:
                    pass

                db.session.delete(item)
                db.session.commit()
            except:
                return redirect(url_for('vendorcreate.itemsforSale', username=current_user.username))
        else:
            return redirect(url_for('vendorcreate.itemsforSale', username=current_user.username))
        return redirect(url_for('vendorcreate.itemsforSale', username=current_user.username))
    else:
        flash("Error", category="danger")
        return redirect(url_for('index'))


@vendorcreate.route('/clone-cloneitem/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def cloneitem(id):
    """
    given an item id, this will create a new folder on storage, and recopy the data with a new id
    :param id:
    :return:
    """
    # get the vendor item to be copied
    now = datetime.utcnow()
    # get item we are cloning
    vendoritem = marketItem.query.get(id)

    if vendoritem:
        if vendoritem.vendor_id == current_user.id:
            # make sure user doesnt have to many listings
            vendoritemcount = db.session\
                .query(marketItem)\
                .filter_by(vendor_id=current_user.id)\
                .count()
            if vendoritemcount < 1000:
                try:
                    priceDecimaled = Decimal(vendoritem.price)
                    p2 = Decimal(vendoritem.shippingprice2)
                    p3 = Decimal(vendoritem.shippingprice3)

                    item = marketItem(
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
                    db.session.add(item)
                    db.session.flush()

                    # IMAGES
                    # Make New image folder
                    getitemlocation = itemlocation(x=item.id)
                    listingdir = '/' + getitemlocation + \
                        '/' + str(item.id) + '/'
                    mkdir_p(path=UPLOADED_FILES_DEST_ITEM + listingdir)
                    # get old directory path
                    oldirectory = UPLOADED_FILES_DEST_ITEM + "/" + \
                        getitemlocation + '/' + str(vendoritem.id) + '/'
                    # new directory path
                    newdirectory = UPLOADED_FILES_DEST + listingdir
                    # lopp over the files and copy them
                    for file_name in os.listdir(oldirectory):
                        full_file_name = os.path.join(oldirectory, file_name)
                        if os.path.isfile(full_file_name):
                            shutil.copy(full_file_name, newdirectory)
                    # query the newly added item, and change the id's accordingly
                    item.stringauctionid = '/' + str(item.id) + '/'

                    getitemlocation = itemlocation(x=item.id)
                    item.stringnodeid = getitemlocation
                    db.session.add(item)
                    db.session.commit()

                    flash("Cloned New Item ", category="success")
                    return redirect(url_for('vendorcreate.itemsforSale'))

                except Exception as e:
                    db.session.rollback()
                    flash("Error.  Could not clone item.", category="danger")
                    redirect((request.args.get('next', request.referrer)))
            else:
                flash("Maximum 100 items allowed per user. ", category="success")
        else:
            flash("Error", category="danger")
            redirect((request.args.get('next', request.referrer)))
    else:
        flash("Error", category="danger")
        redirect((request.args.get('next', request.referrer)))


@vendorcreate.route('/need-a-vacation/', methods=['GET', 'POST'])
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


@vendorcreate.route('/deletepicture/<int:id>/<string:img>', methods=['GET', 'POST'])
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
                    pathtofile = os.path.join(
                        UPLOADED_FILES_DEST, link, specific_folder, img)
                    pathtofile, file_extension = os.path.splitext(pathtofile)

                    ext_1 = '_225x'
                    ext_2 = '_500x'

                    file0 = os.path.join(pathtofile, ".", file_extension)
                    file1 = os.path.join(
                        pathtofile, ext_1, ".", file_extension)
                    file2 = os.path.join(
                        pathtofile, ext_2, ".", file_extension)
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
                                os.remove(file2)
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
                                os.remove(file2)
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
                                os.remove(file2)
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
                                os.remove(file2)
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
                                os.remove(file2)
                            except Exception:
                                pass

                        else:
                            redirect(
                                (request.args.get('next', request.referrer)))
                        db.session.commit()
                    redirect((request.args.get('next', request.referrer)))
                except Exception:
                    redirect((request.args.get('next', request.referrer)))
            else:
                redirect((request.args.get('next', request.referrer)))
        else:
            flash("Error", category="danger")
            return redirect(url_for('index'))
    except:
        redirect((request.args.get('next', request.referrer)))


def deleteimg_noredirect(id, img):
    try:
        vendoritem = marketItem.query.get(id)
        if vendoritem:
            if vendoritem.vendor_id == current_user.id:
                try:
                    specific_folder = str(vendoritem.id)
                    link = 'listing'
                    pathtofile = os.path.join(
                        UPLOADED_FILES_DEST, link, specific_folder, img)
                    pathtofile, file_extension = os.path.splitext(pathtofile)
                    ext_1 = '_225x'
                    ext_2 = '_500x'
                    file0 = os.path.join(pathtofile, ".", file_extension)
                    file1 = os.path.join(
                        pathtofile + ext_1, ".", file_extension)
                    file2 = os.path.join(
                        pathtofile + ext_2, ".", file_extension)

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
                                os.remove(file2)
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
                                os.remove(file2)
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
                                os.remove(file2)
                            except Exception:
                                pass

                        else:
                            pass
                        db.session.commit()
                except Exception:
                    flash("Error", category="danger")
                    return redirect(url_for('index'))
        else:
            flash("Error", category="danger")
            return redirect(url_for('index'))
    except:
        return redirect(url_for('index', username=current_user.username))
