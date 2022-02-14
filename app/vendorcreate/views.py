from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.vendorcreate import vendorcreate
import shutil
import os
import csv
from app import UPLOADED_FILES_DEST, UPLOADED_FILES_DEST_ITEM
from werkzeug.datastructures import CombinedMultiDict
from werkzeug.utils import secure_filename
from decimal import Decimal
from app.search.searchfunction import headerfunctions_vendor
from flask_paginate import Pagination, get_page_args
from app.common.decorators import \
    website_offline, \
    login_required, \
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
from app.classes.auth import Auth_User

from app.classes.item import \
    Item_MarketItem
from app.classes.vendor import \
    Vendor_EbaySearchItem

from app.classes.wallet_bch import *
from app.vendor.images.image_forms import image1, image2, image3, image4, image5


@vendorcreate.route('/trade-options/')
@website_offline
@login_required
@vendoraccount_required
def vendorcreate_sell_options():
    """
    Returns the page with buttons to post type of item/ad
    :return:
    """
    return render_template('/vendor/tradeoptions.html')


@vendorcreate.route('/myitems', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorcreate_items_for_sale():
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
    sale = db.session.query(Item_MarketItem).filter(Item_MarketItem.vendor_id == user.id).order_by(
        Item_MarketItem.total_sold.desc(), Item_MarketItem.online.desc(), Item_MarketItem.id.desc())


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
                    .query(Item_MarketItem)\
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
                        if len(specific_item.image_one) < 10:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash(
                                f"Item# {str(specific_item.id)} Doesnt have a main image. Cannot put item online.", category="danger")
                            see_if_changes.append(1)

                        if specific_item.destination_country_one == '0':
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash(
                                f"Item #{str(specific_item.id)} Doesnt have a destination country. Cannot put item online.", category="danger")
                            see_if_changes.append(1)

                        if specific_item.origin_country == '0':
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash(
                                f"Item #{str(specific_item.id)} Doesnt have an origin. Cannot put item online.", category="danger")
                            see_if_changes.append(1)

                        if specific_item.item_count <= 0:
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

                        if len(specific_item.item_title) < 10:
                            specific_item.online = 0
                            db.session.add(specific_item)
                            flash(
                                f"Item# {str(specific_item.id)} Doesnt have a proper title. Cannot put item online.", category="danger")
                            see_if_changes.append(1)

                        if specific_item.shipping_two == 1:
                            if Decimal(specific_item.shipping_price_2) > .01:
                                if len(specific_item.shipping_info_2) >= 2:
                                    pass
                            else:
                                specific_item.shipping_two = 0
                                db.session.add(specific_item)
                                flash(
                                    f"Item# + {str(specific_item.id)} Doesnt have a proper shipping price 2.", category="danger")
                                see_if_changes.append(1)

                        if specific_item.shipping_three == 1:
                            if Decimal(specific_item.shipping_price_3) > .01:
                                if len(specific_item.shipping_info_3) >= 2:
                                    pass
                            else:
                                specific_item.shipping_three = 0
                                db.session.add(specific_item)
                                flash(
                                    f"Item #{str(specific_item.id)} Doesnt have a proper shipping info 3 or price.", category="danger")
                                see_if_changes.append(1)

                        if specific_item.shipping_free == 0 \
                                and specific_item.shipping_two == 0 \
                                and specific_item.shipping_three == 0:
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

    return render_template('/vendor/itemsforsale/vendoritemsforsale.html',
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
def vendorcreate_ebay_importer():
    # variables
    now = datetime.utcnow()
    id_pic1 = id_generator_picture1()

    # forms
    form = UploadEbayForm()

    # queries
    user = db.session\
        .query(Auth_User)\
        .filter_by(id=current_user.id)\
        .first()
    getalluploads = db.session\
        .query(Vendor_EbaySearchItem)\
        .filter_by(user_id=current_user.id)\
        .order_by(Vendor_EbaySearchItem.dateadded.desc())\
        .limit(100)
    getalluploadscount = db.session\
        .query(Vendor_EbaySearchItem)\
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

                                newitem = Vendor_EbaySearchItem(
                                    dateadded=now,
                                    user_id=current_user.id,
                                    itemebayid=ebayitemid,
                                    itemtitle=ebaytitle,
                                    itemprice=dollars_dec,
                                    itemquantity=quantity,
                                    item_condition=protoscondition,
                                    itemcategory=category,
                                    status=0,
                                )

                                db.session.add(newitem)

                            db.session.commit()
                            flash("Your auctions will be added within an hour.  If there are any issues,"
                                  "please report them to customer feedback.", category="success")
                            return redirect(url_for('vendorcreate.vendorcreate_ebay_importer'))
                    else:
                        flash("Form Error. Only CSV's allowed.",
                              category="danger")
                        return redirect(url_for('vendorcreate.vendorcreate_ebay_importer'))
                else:
                    flash("Form Error. Only CSV's allowed.", category="danger")
                    return redirect(url_for('vendorcreate.vendorcreate_ebay_importer'))
            else:
                flash("Form Error. Only CSV's allowed.", category="danger")
                return redirect(url_for('vendorcreate.vendorcreate_ebay_importer'))
        elif form.delete.data:
            for f in getalluploads:
                if f.user_id == current_user.id:
                    db.session.delete(f)
            db.session.commit()
            flash("Items deleted ", category="danger")
            return redirect(url_for('vendorcreate.vendorcreate_ebay_importer'))
        else:
            flash("Form Error. Only CSV's allowed.", category="danger")
            return redirect(url_for('vendorcreate.vendorcreate_ebay_importer'))

    return render_template('/vendor/tools/vendorcreate_ebay_importer.html',
                           form=form,
                           user=user,
                           now=now,
                           getalluploads=getalluploads,
                           getalluploadscount=getalluploadscount
                           )


@vendorcreate.route('/vendor-vendorcreate_edit_item/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorcreate_edit_item(id):
    """
    Edits a specific item given an id
    :param id:
    :return:
    """
    now = datetime.utcnow()
    item = db.session\
        .query(Item_MarketItem)\
        .filter_by(id=id)\
        .first()
    if item:
        user = db.session\
            .query(Auth_User)\
            .filter_by(id=current_user.id)\
            .first()
        if item.vendor_id == user.id:

            vendorcreateItem = add_product_form_factory(item=item)

            form = vendorcreateItem(
                digital_currency_2=item.digital_currency_2,
                digital_currency_3=item.digital_currency_2,
                item_title=item.item_title,
                item_description=item.item_description,
                item_refund_policy=item.item_refund_policy,
                price=item.price,
                currency=item.currency,
                item_count=item.item_count,
                origin_country=item.origin_country,
                destination1=item.destination_country_one,
                destination2=item.destination_country_two,
                destination3=item.destination_country_three,
                destination4=item.destination_country_four,
                destination5=item.destination_country_five,
                item_condition=item.item_condition,
                keywords=item.keywords,
                return_this_item=item.return_allowed,
                shipping_free=item.shipping_free,
                shipping_info_0=item.shipping_info_0,
                shipping_day_least_0=item.shipping_day_least_0,
                shipping_day_most_0=item.shipping_day_most_0,
                shipping_info_2=item.shipping_info_2,
                shipping_price_2=item.shipping_price_2,
                shipping_day_least_2=item.shipping_day_least_2,
                shipping_day_most_2=item.shipping_day_most_2,
                shipping_info_3=item.shipping_info_3,
                shipping_price_3=item.shipping_price_3,
                shipping_day_least_3=item.shipping_day_least_3,
                shipping_day_most_3=item.shipping_day_most_3,
                not_shipping_1=item.not_shipping_1,
                not_shipping_2=item.not_shipping_2,
                not_shipping_3=item.not_shipping_3,
                not_shipping_4=item.not_shipping_4,
                not_shipping_5=item.not_shipping_5,
                not_shipping_6=item.not_shipping_6,
                details=item.details,
                details_1=item.details_1,
                details_1_answer=item.details_1_answer,
                details_2=item.details_2,
                details_2_answer=item.details_2_answer,
                details_3=item.details_3,
                details_3_answer=item.details_3_answer,
                details_4=item.details_4,
                details_4_answer=item.details_4_answer,
                details_5=item.details_5,
                details_5_answer=item.details_5_answer,
                shipping_three=item.shipping_three,
                shipping_two=item.shipping_two,
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

                    image1(formdata=form.image_one1.data,
                           item=item,
                           directoryifitemlisting=directoryifitemlisting)
                    image2(formdata=form.image_two.data,
                           item=item,
                           directoryifitemlisting=directoryifitemlisting)
                    image3(formdata=form.image_three.data,
                           item=item,
                           directoryifitemlisting=directoryifitemlisting)
                    image4(formdata=form.image_four.data,
                           item=item,
                           directoryifitemlisting=directoryifitemlisting)
                    image5(formdata=form.image_five.data,
                           item=item,
                           directoryifitemlisting=directoryifitemlisting)

                    if form.shipping_two.data is True:
                        shipping_two = 1
                    else:
                        shipping_two = 0

                    if form.shipping_three.data is True:
                        shipping_three = 1
                    else:
                        shipping_three = 0

                    if form.btc_cash_accepted.data is True:
                        digital_currency_3 = 1
                    else:
                        digital_currency_3 = 0

                    if form.return_this_item.data is True:
                        return_allowed = 1
                    else:
                        return_allowed = 0

                    # get category and subcategory
                    if form.category_edit.data:
                        categoryfull = form.category_edit.data
                        cat0 = categoryfull.cat_id
                        category_name_0 = categoryfull.name
                    else:
                        cat0 = 0
                        category_name_0 = ''

                    # Get currency from query
                    if form.currency1.data:
                        currencyfull = form.currency1.data
                        cur = currencyfull.code
                    else:
                        cur = 0

                    # get item condition query
                    if form.item_condition_edit.data:
                        item_conditionfull = form.item_condition_edit.data
                        item_condition = item_conditionfull.value
                    else:
                        item_condition = 0

                    # get iitem_count query
                    if form.item_count_edit.data:
                        item_countfull = form.item_count_edit.data
                        item_count = item_countfull.value
                    else:
                        item_count = 0

                    # get origin country query
                    if form.origin_country_1.data:
                        origin_countryfull = form.origin_country_1.data
                        origin_country = origin_countryfull.numericcode
                    else:
                        origin_country = 0

                    # get destination 1
                    if form.destination11.data:
                        getdest1full = form.destination11.data
                        getdest1 = getdest1full.numericcode
                    else:
                        getdest1 = 0

                    # get destination2
                    if form.destination21.data:
                        getdest2full = form.destination21.data
                        getdest2 = getdest2full.numericcode
                    else:
                        getdest2 = 0

                    # getdestination 3
                    if form.destination31.data:
                        getdest3full = form.destination31.data
                        getdest3 = getdest3full.numericcode
                    else:
                        getdest3 = 0

                    # getdestination 4
                    if form.destination41.data:
                        getdest4full = form.destination41.data
                        getdest4 = getdest4full.numericcode
                    else:
                        getdest4 = 0

                    # getdestination 5
                    if form.destination51.data:
                        getdest5full = form.destination51.data
                        getdest5 = getdest5full.numericcode
                    else:
                        getdest5 = 0

                    # get get not shipping 1
                    if form.not_shipping_11.data:
                        getnotship1full = form.not_shipping_11.data
                        getnotship1 = getnotship1full.value
                    else:
                        getnotship1 = 0

                    # get get not shipping 2
                    if form.not_shipping_21.data:
                        getnotship2full = form.not_shipping_21.data
                        getnotship2 = getnotship2full.value
                    else:
                        getnotship2 = 0

                    # get get not shipping 3
                    if form.not_shipping_31.data:
                        getnotship3full = form.not_shipping_31.data
                        getnotship3 = getnotship3full.value
                    else:
                        getnotship3 = 0

                    # get get not shipping 4
                    if form.not_shipping_41.data:
                        getnotship4full = form.not_shipping_41.data
                        getnotship4 = getnotship4full.value
                    else:
                        getnotship4 = 0

                    # get get not shipping 5
                    if form.not_shipping_51.data:
                        getnotship5full = form.not_shipping_51.data
                        getnotship5 = getnotship5full.value
                    else:
                        getnotship5 = 0

                    # get get not shipping 6
                    if form.notshipping61.data:
                        getnotship6full = form.notshipping61.data
                        getnotship6 = getnotship6full.value
                    else:
                        getnotship6 = 0

                    # get shippindayleast 0
                    if form.shipping_day_least_01.data:
                        getshipdayleastfull0 = form.shipping_day_least_01.data
                        getshipdayleast0 = getshipdayleastfull0.value
                    else:
                        getshipdayleast0 = 0

                    # get shipping day most 0
                    if form.shipping_day_most01.data:
                        getshippingdaymostfull0 = form.shipping_day_most01.data
                        getshipping_day_most0 = getshippingdaymostfull0.value
                    else:
                        getshipping_day_most0 = 0

                    # get shippindayleast 2
                    if form.shipping_day_least_21.data:
                        getshipdayleastfull2 = form.shipping_day_least_21.data
                        getshipdayleast2 = getshipdayleastfull2.value
                    else:
                        getshipdayleast2 = 0

                    # get shipping day most 2
                    if form.shipping_day_most_21.data:
                        getshippingdaymostfull2 = form.shipping_day_most_21.data
                        getshipping_day_most_2 = getshippingdaymostfull2.value
                    else:
                        getshipping_day_most_2 = 0

                    # get shippindayleast 3
                    if form.shipping_day_least_31.data:
                        getshipdayleastfull3 = form.shipping_day_least_31.data
                        getshipdayleast3 = getshipdayleastfull3.value
                    else:
                        getshipdayleast3 = 0

                    # get shipping day most 3
                    if form.shipping_day_most_31.data:
                        getshippingdaymostfull3 = form.shipping_day_most_31.data
                        getshipping_day_most_3 = getshippingdaymostfull3.value
                    else:
                        getshipping_day_most_3 = 0

                    # Form data
                    item.category_name_0 = category_name_0
                    item.category_id_0 = cat0
                    item.digital_currency_1 = 0
                    item.digital_currency_2 = 0
                    item.digital_currency_3 = digital_currency_3
                    item.origin_country = origin_country
                    item.destination_country_one = getdest1
                    item.destination_country_two = getdest2
                    item.destination_country_three = getdest3
                    item.destination_country_four = getdest4
                    item.destination_country_five = getdest5
                    item.item_condition = item_condition
                    item.item_title = form.item_title.data
                    item.item_count = item_count
                    item.item_description = form.item_description.data
                    item.item_refund_policy = form.item_refund_policy.data
                    item.price = form.price.data
                    item.currency = cur
                    item.keywords = form.keywords.data
                    item.return_allowed = return_allowed
                    item.shipping_free = form.shipping_free.data
                    item.shipping_two = shipping_two
                    item.shipping_three = shipping_three
                    item.shipping_info_0 = form.shipping_info_0.data
                    item.shipping_day_least_0 = getshipdayleast0
                    item.shipping_day_most_0 = getshipping_day_most0
                    item.shipping_info_2 = form.shipping_info_2.data
                    item.shipping_price_2 = form.shipping_price_2.data
                    item.shipping_day_least_2 = getshipdayleast2
                    item.shipping_day_most_2 = getshipping_day_most_2
                    item.shipping_info_3 = form.shipping_info_3.data
                    item.shipping_price_3 = form.shipping_price_3.data
                    item.shipping_day_least_3 = getshipdayleast3
                    item.shipping_day_most_3 = getshipping_day_most_3
                    item.not_shipping_1 = getnotship1
                    item.not_shipping_2 = getnotship2
                    item.not_shipping_3 = getnotship3
                    item.not_shipping_4 = getnotship4
                    item.not_shipping_5 = getnotship5
                    item.not_shipping_6 = getnotship6
                    item.details_1 = form.details.data
                    item.details_1_answer = form.details_1_answer.data
                    item.details_2 = form.details_2.data
                    item.details_2_answer = form.details_2_answer.data
                    item.details_3 = form.details_3.data
                    item.details_3_answer = form.details_3_answer.data
                    item.details_4 = form.details_4.data
                    item.details_4_answer = form.details_4_answer.data
                    item.details_5 = form.details_5.data
                    item.details_5_answer = form.details_5_answer.data

                    db.session.add(item)
                    db.session.commit()

                    flash(f"Updated: Item #{str(item.id)}", category="success")
                    return redirect(url_for('vendorcreate.vendorcreate_items_for_sale'))

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
@vendoraccount_required
def vendorcreate_delete_item(id):
    """
    Delete all images and the item data from database
    :param id:
    :return:
    """
    ext_1 = '_225x.jpg'
    ext_2 = '_500x.jpg'
    file_extension1 = '.jpg'
    item = Item_MarketItem.query.get(id)
    if item:
        if item.vendor_id == current_user.id:
            # gets the node for the folder
            getitemlocation = itemlocation(x=item.id)
            # Gets items folder id on server
            specific_folder = str(item.id)

            # returns path of the folder minus extension at end
            pathtofile1 = os.path.join(
                UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, item.image_one)
            pathtofile2 = os.path.join(
                UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, item.image_two)
            pathtofile3 = os.path.join(
                UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, item.image_three)
            pathtofile4 = os.path.join(
                UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, item.image_four)
            pathtofile5 = os.path.join(
                UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, item.image_five)

            if len(item.image_one) > 10:
                file00 = pathtofile1 + file_extension1
                file01 = pathtofile1 + ext_1
                file02 = pathtofile1 + ext_2
                try:
                    os.remove(file00)
                except:
                    pass
                try:
                    os.remove(file01)
                    os.remove(file02)
                except:
                    pass

            if len(item.image_two) > 10:
                file10 = pathtofile2 + file_extension1
                file11 = pathtofile2 + ext_1
                file12 = pathtofile2 + ext_2
                try:
                    os.remove(file10)
                except:
                    pass
                try:
                    os.remove(file11)
                    os.remove(file12)
                except:
                    pass

            if len(item.image_three) > 10:
                file20 = pathtofile3 + file_extension1
                file21 = pathtofile3 + ext_1
                file22 = pathtofile3 + ext_2
                try:
                    os.remove(file20)
                except:
                    pass
                try:
                    os.remove(file21)
                    os.remove(file22)
                except:
                    pass

            if len(item.image_four) > 10:
                file30 = pathtofile4 + file_extension1
                file31 = pathtofile4 + ext_1
                file32 = pathtofile4 + ext_2
                try:
                    os.remove(file30)
                except:
                    pass
                try:
                    os.remove(file31)
                    os.remove(file32)
                except:
                    pass

            if len(item.image_five) > 10:
                file40 = pathtofile5 + file_extension1
                file41 = pathtofile5 + ext_1
                file42 = pathtofile5 + ext_2
                try:
                    os.remove(file40)
                except:
                    pass
                try:
                    os.remove(file41)
                    os.remove(file42)
                except:
                    pass

            db.session.delete(item)
            db.session.commit()

        else:
            return redirect(url_for('vendorcreate.vendorcreate_items_for_sale', username=current_user.username))
        return redirect(url_for('vendorcreate.vendorcreate_items_for_sale', username=current_user.username))
    else:
        flash("Error", category="danger")
        return redirect(url_for('index'))


@vendorcreate.route('/clone-cloneitem/<int:id>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorcreate_clone_item(id):
    """
    given an item id, this will create a new folder on storage, and recopy the data with a new id
    :param id:
    :return:
    """
    # get item we are cloning
    vendoritem = Item_MarketItem.query.get(id)

    if vendoritem:
        if vendoritem.vendor_id == current_user.id:
            # make sure user doesnt have to many listings
            vendoritem_count = db.session\
                .query(Item_MarketItem)\
                .filter_by(vendor_id=current_user.id)\
                .count()
            if vendoritem_count < 1000:

                item = Item_MarketItem(
                    string_node_id=vendoritem.string_node_id,
                    created=datetime.utcnow(),
                    vendor_name=current_user.username,
                    vendor_id=current_user.id,
                    origin_country=vendoritem.origin_country,
                    destination_country_one=vendoritem.destination_country_one,
                    destination_country_two=vendoritem.destination_country_two,
                    destination_country_three=vendoritem.destination_country_three,
                    destination_country_four=vendoritem.destination_country_four,
                    destination_country_five=vendoritem.destination_country_five,
                    return_allowed=vendoritem.return_allowed,
                    item_title=vendoritem.item_title,
                    item_count=0,
                    item_description=vendoritem.item_description,
                    item_refund_policy=vendoritem.item_refund_policy,
                    price=vendoritem.price,
                    currency=vendoritem.currency,
                    image_one=vendoritem.image_one,
                    image_two=vendoritem.image_two,
                    image_three=vendoritem.image_three,
                    image_four=vendoritem.image_four,
                    image_five=vendoritem.image_five,
                    item_condition=vendoritem.item_condition,
                    total_sold=0,
                    keywords=vendoritem.keywords,
                    shipping_free=vendoritem.shipping_free,
                    shipping_info_0=vendoritem.shipping_info_0,
                    shipping_day_least_0=vendoritem.shipping_day_least_0,
                    shipping_day_most_0=vendoritem.shipping_day_most_0,
                    shipping_info_2=vendoritem.shipping_info_2,
                    shipping_price_2=vendoritem.shipping_price_2,
                    shipping_day_least_2=vendoritem.shipping_day_least_2,
                    shipping_day_most_2=vendoritem.shipping_day_most_2,
                    shipping_info_3=vendoritem.shipping_info_3,
                    shipping_price_3=vendoritem.shipping_price_3,
                    shipping_day_least_3=vendoritem.shipping_day_least_3,
                    shipping_day_most_3=vendoritem.shipping_day_most_3,
                    not_shipping_1=vendoritem.not_shipping_1,
                    not_shipping_2=vendoritem.not_shipping_2,
                    not_shipping_3=vendoritem.not_shipping_3,
                    not_shipping_4=vendoritem.not_shipping_4,
                    not_shipping_5=vendoritem.not_shipping_5,
                    not_shipping_6=vendoritem.not_shipping_6,
                    details=vendoritem.details,
                    details_1=vendoritem.details_1,
                    details_1_answer=vendoritem.details_1_answer,
                    details_2=vendoritem.details_2,
                    details_2_answer=vendoritem.details_2_answer,
                    details_3=vendoritem.details_3,
                    details_3_answer=vendoritem.details_3_answer,
                    details_4=vendoritem.details_4,
                    details_4_answer=vendoritem.details_4_answer,
                    details_5=vendoritem.details_5,
                    details_5_answer=vendoritem.details_5_answer,
                    shipping_two=vendoritem.shipping_two,
                    shipping_three=vendoritem.shipping_three,
                    view_count=0,
                    item_rating=0,
                    review_count=0,
                    online=0,
                    ad_item=0,
                    ad_item_level=0,
                    ad_item_timer=datetime.utcnow(),
                    category_name_0=vendoritem.category_name_0,
                    category_id_0=vendoritem.category_id_0,
                    digital_currency_1=0,
                    digital_currency_2=1,
                    digital_currency_3=0,
                )
                db.session.add(item)
                db.session.flush()

                # IMAGES
                # get location of node
                getitemlocation = itemlocation(x=item.id)
                # get directory of item to be closed
                listingdir = '/' + getitemlocation + \
                    '/' + str(item.id) + '/'
                # make the directory
                mkdir_p(path=UPLOADED_FILES_DEST_ITEM + listingdir)
                # get old directory path
                oldirectory = UPLOADED_FILES_DEST_ITEM + '/' + \
                    getitemlocation + '/' + str(vendoritem.id) + '/'
                # new directory path
                newdirectory = UPLOADED_FILES_DEST_ITEM + listingdir
                # loop over the files and copy them
                for file_name in os.listdir(oldirectory):
                    full_file_name = os.path.join(oldirectory, file_name)
                    if os.path.isfile(full_file_name):
                        shutil.copy(full_file_name, newdirectory)

                # query the newly added item, and change the id's accordingly
                item.string_auction_id = '/' + str(item.id) + '/'
                item.string_node_id = getitemlocation

                # commit to db
                db.session.add(item)
                db.session.commit()

                flash("Cloned New Item ", category="success")
                return redirect(url_for('vendorcreate.vendorcreate_items_for_sale'))

            else:
                flash("Maximum 100 items allowed per user. ", category="success")
                return redirect(url_for('vendorcreate.vendorcreate_items_for_sale'))
        else:
            flash("Error", category="danger")
            return redirect(url_for('vendorcreate.vendorcreate_items_for_sale'))
    else:
        flash("Error", category="danger")
        return redirect(url_for('vendorcreate.vendorcreate_items_for_sale'))


@vendorcreate.route('/need-a-vacation/', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorcreate_vacation():
    """
    Vacation mode allows user to turn off all items instantly.  In the future
    add a message perhaps and keep items online
    :return:
    """
    # Turn off all items, and remove users visibility
    user = db.session\
        .query(Auth_User)\
        .filter_by(username=current_user.username)\
        .first()

    # get physical items
    aitems = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.vendor_id == current_user.id)\
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
    return redirect(url_for('auth.my_account', username=current_user.username))


@vendorcreate.route('/deletepicture/<int:id>/<string:img>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def vendorcreate_delete_img(id, img):
    """
    gets specific id and image, it will delete on the server accordingly
    :param id:
    :param img:
    :return:
    """

    item = db.session\
        .query(Item_MarketItem)\
        .filter_by(id=id)\
        .first()
    if item:
        if item.vendor_id == current_user.id:
            # get folder for item id
            specific_folder = str(item.id)
            # get node location
            getitemlocation = itemlocation(x=item.id)
            # get path of item on folder
            pathtofile = os.path.join(
                UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, img)

            ext_1 = '_225x.jpg'
            ext_2 = '_500x.jpg'
            file0 = pathtofile + ".jpg"
            file1 = pathtofile + ext_1
            file2 = pathtofile + ext_2

            if len(img) > 20:

                if item.image_one == img:

                    os.remove(file0)
                    os.remove(file1)
                    os.remove(file2)
                    item.image_one = '0'
                    db.session.add(item)
                    db.session.commit()
                    return redirect(url_for('vendorcreate.vendorcreate_edit_item', id=item.id))
                elif item.image_two == img:
                    os.remove(file0)
                    os.remove(file1)
                    os.remove(file2)
                    item.image_two = '0'
                    db.session.add(item)
                    db.session.commit()
                    return redirect(url_for('vendorcreate.vendorcreate_edit_item', id=item.id))
                elif xitem.image_three3 == img:
                    os.remove(file0)
                    os.remove(file1)
                    os.remove(file2)
                    item.image_three = '0'
                    db.session.add(item)
                    db.session.commit()
                    return redirect(url_for('vendorcreate.vendorcreate_edit_item', id=item.id))
                elif item.image_four == img:
                    os.remove(file0)
                    os.remove(file1)
                    os.remove(file2)
                    item.image_four = '0'
                    db.session.add(item)
                    db.session.commit()
                    return redirect(url_for('vendorcreate.vendorcreate_edit_item', id=item.id))
                elif item.image_five == img:
                    os.remove(file0)
                    os.remove(file1)
                    os.remove(file2)
                    item.image_five = '0'
                    db.session.add(item)
                    db.session.commit()
                    return redirect(url_for('vendorcreate.vendorcreate_edit_item', id=item.id))
                else:
                    flash("No Matching Images", category="danger")
                    return redirect(url_for('vendorcreate.vendorcreate_edit_item', id=item.id))
            else:
                print("down 1")
                flash("Incorrect Image Size", category="danger")
                return redirect(url_for('vendorcreate.vendorcreate_edit_item', id=item.id))
        else:
            flash("Incorrect user.", category="danger")
            return redirect(url_for('vendorcreate.vendorcreate_edit_item', id=item.id))
    else:
        flash("Error", category="danger")
        return redirect(url_for('vendorcreate.vendorcreate_edit_item', id=item.id))


def deleteimg_noredirect(id, img):
    try:
        vendoritem = Item_MarketItem.query.get(id)
        if vendoritem:
            if vendoritem.vendor_id == current_user.id:
                try:
                    item = db.session\
                        .query(Item_MarketItem)\
                        .filter_by(id=id)\
                        .first()
                    # get folder for item id
                    specific_folder = str(item.id)
                    # get node location
                    getitemlocation = itemlocation(x=item.id)
                    # get path of item on folder
                    pathtofile = os.path.join(
                        UPLOADED_FILES_DEST_ITEM, getitemlocation, specific_folder, img)

                    ext_1 = '_225x.jpg'
                    ext_2 = '_500x.jpg'
                    file0 = pathtofile + ".jpg"
                    file1 = pathtofile + ext_1
                    file2 = pathtofile + ext_2

                    if len(img) > 20:
                        if vendoritem.image_one == img:
                            vendoritem.image_one = '0'
                            db.session.add(vendoritem)
                            os.remove(file0)
                            os.remove(file1)
                            db.session.commit()
                        elif vendoritem.image_two == img:
                            vendoritem.image_two = '0'
                            db.session.add(vendoritem)
                            os.remove(file0)
                            os.remove(file1)
                            db.session.commit()
                        elif vendoritem.image_three == img:
                            vendoritem.image_three = '0'
                            db.session.add(vendoritem)
                            os.remove(file0)
                            os.remove(file1)
                            os.remove(file2)
                            db.session.commit()
                        elif vendoritem.image_four == img:
                            vendoritem.image_four = '0'
                            db.session.add(vendoritem)
                            os.remove(file0)
                            os.remove(file1)
                            os.remove(file2)
                            db.session.commit()
                        elif vendoritem.image_five == img:
                            vendoritem.image_five = '0'
                            db.session.add(vendoritem)
                            os.remove(file0)
                            os.remove(file1)
                            os.remove(file2)
                            db.session.commit()
                        else:
                            pass
                    else:
                        pass
                except Exception:
                    flash("Error", category="danger")
                    return redirect(url_for('index'))
            else:
                pass
        else:
            flash("Error", category="danger")
            return redirect(url_for('index'))
    except:
        return redirect(url_for('index', username=current_user.username))
