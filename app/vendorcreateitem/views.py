from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.vendorcreateitem import vendorcreateitem
from app import UPLOADED_FILES_DEST_ITEM
from werkzeug.datastructures import CombinedMultiDict
import os
from app.common.decorators import \
    website_offline, \
    login_required, \
    vendoraccount_required
from app.common.functions import \
    mkdir_p, \
    itemlocation
from app.common.functions import mkdir_p

# forms
from app.vendorcreateitem.forms import \
    add_product_info, \
    CreateItemImages, \
    CreateInfoDescription, \
    add_product_shipping

# models
from app.classes.item import \
    marketitem
from app.classes.wallet_bch import *

# images
from app.vendor.images.image_forms import image1, image2, image3, image4, image5


@vendorcreateitem.route('/create-item-info', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def create_item_info():
    """
    Vendor creates an item to be listed
    :return:
    """
    now = datetime.utcnow()

    # item = 0 creating item       item = 1 editing item
    vendor_create_item_info = add_product_info(item=0)
    form = vendor_create_item_info(
        CombinedMultiDict((request.files, request.form)))

    if request.method == 'POST':
        if form.validate_on_submit():
            if form.btc_accepted.data is True:
                digital_currency_2 = 1
            else:
                digital_currency_2 = 0

            if form.btc_cash_accepted.data is True:
                digital_currency_3 = 1
            else:
                digital_currency_3 = 0

            # Get currency from query
            if form.currency.data:
                currencyfull = form.currency.data
                cur = currencyfull.code
            else:
                cur = 0

            # get item condition query
            if form.item_condition.data:
                item_conditionfull = form.item_condition.data
                item_condition = item_conditionfull.value
            else:
                item_condition = 0

            # get item_count query
            if form.item_count.data:
                item_countfull = form.item_count.data
                item_count = item_countfull.value
            else:
                item_count = 0

            # category query
            if form.category.data:
                categoryfull = form.category.data
                cat0 = categoryfull.id
                category_name_0 = categoryfull.name
            else:
                cat0 = 0
                category_name_0 = ''

            # create image of item in database
            item = marketitem(
                string_node_id=1,
                category_name_0=category_name_0,
                category_id_0=cat0,
                digital_currency_1=0,
                digital_currency_2=digital_currency_2,
                digital_currency_3=digital_currency_3,
                created=now,
                vendor_name=current_user.username,
                vendor_id=current_user.id,
                origin_country=0,
                destination_country_one=0,
                destination_country_two=0,
                destination_country_three=0,
                destination_country_four=0,
                destination_country_five=0,
                item_title=form.item_title.data,
                item_count=item_count,
                item_description='',
                item_refund_policy='',
                price=form.price.data,
                currency=cur,
                item_condition=item_condition,
                total_sold=0,
                keywords=form.keywords.data,
                return_allowed=0,
                shipping_free=True,
                shipping_info_0='',
                shipping_two=0,
                shipping_three=0,
                shipping_day_least_0=0,
                shipping_day_most_0=0,
                shipping_info_2='',
                shipping_price_2=0,
                shipping_day_least_2=0,
                shipping_day_most_2=0,
                shipping_info_3='',
                shipping_price_3=0,
                shipping_day_least_3=0,
                shipping_day_most_3=0,
                not_shipping_1=0,
                not_shipping_2=0,
                not_shipping_3=0,
                not_shipping_4=0,
                not_shipping_5=0,
                not_shipping_6=0,
                details=False,
                details_1='',
                details_1_answer='',
                details_2='',
                details_2_answer='',
                details_3='',
                details_3_answer='',
                details_4='',
                details_4_answer='',
                details_5='',
                details_5_answer='',
                view_count=0,
                item_rating=0,
                review_count=0,
                online=0,
                ad_item=0,
                ad_item_level=0,
                ad_item_timer=now,
            )

            # add image to database
            db.session.add(item)
            db.session.flush()

            item.auctionid = item.id
            item.string_auction_id = '/' + str(item.id) + '/'

            db.session.add(item)
            db.session.commit()

            flash("Created New Item ", category="success")
            return redirect(url_for('vendorcreateitem.create_item_images', itemid=item.id))
        else:
            return redirect(url_for('vendorcreateitem.create_item_info', itemid=item.id))
    return render_template('/vendor/create_item/item_info.html', form=form)


@vendorcreateitem.route('/create-an-item-images/<int:itemid>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def create_item_images(itemid):
    """
    Vendor creates an item to be listed
    :return:
    """
    # first see if they arnt spamming the site.  In future set to balance or level
    # current total items to prevent scripters
    # item = 0 creating item       item = 1 editing item

    form = CreateItemImages(CombinedMultiDict((request.files, request.form)))

    item = db.session \
        .query(marketitem) \
        .filter(marketitem.id == itemid, marketitem.vendor_id == current_user.id) \
        .first_or_404()

    if request.method == 'POST':
        if form.validate_on_submit():
            # node location
            getimagesubfolder = itemlocation(x=item.id)
            # item location by id
            item.string_node_id = getimagesubfolder
            # directory of image
            directoryifitemlisting = os.path.join(
                UPLOADED_FILES_DEST_ITEM, getimagesubfolder, (str(item.id)))
            # make directory
            mkdir_p(path=directoryifitemlisting)
            # upload images
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

            # convert image sizes
            db.session.add(item)
            db.session.commit()

            return redirect(url_for('vendorcreateitem.create_item_description', itemid=item.id))
        else:
            flash("Form Error", category="danger")
            return redirect(url_for('vendorcreateitem.create_item_description', username=current_user.username))
    return render_template('/vendor/create_item/item_images.html', form=form)


@vendorcreateitem.route('/create-an-item-description/<int:itemid>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def create_item_description(itemid):
    """
    Vendor creates an item to be listed
    :return:
    """
    form = CreateInfoDescription()

    item = db.session \
        .query(marketitem) \
        .filter(marketitem.id == itemid, marketitem.vendor_id == current_user.id) \
        .first_or_404()
    # item = 0 creating item       item = 1 editing item

    if request.method == 'POST':
        if form.validate_on_submit():
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

            item.item_description = form.item_description.data

            db.session.add(item)
            db.session.commit()

            return redirect(url_for('vendorcreateitem.create_item_shipping', itemid=item.id))
        else:
            flash("Form Error", category="danger")
            return redirect(url_for('vendorcreateitem.create_item_shipping', itemid=item.id))
    return render_template('/vendor/create_item/item_description.html', form=form)


@vendorcreateitem.route('/create-an-item-shipping/<int:itemid>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def create_item_shipping(itemid):
    """
    Vendor creates an item to be listed
    :return:
    """

    # item = 0 creating item       item = 1 editing item
    vendor_create_shipping = add_product_shipping(item=0)
    form = vendor_create_shipping(CombinedMultiDict(
        (request.files, request.form)))

    item = db.session \
        .query(marketitem) \
        .filter(marketitem.id == itemid, marketitem.vendor_id == current_user.id) \
        .first_or_404()

    if request.method == 'POST' and current_user.vendor_account == 1:
        if form.validate_on_submit():

            if form.origin_country.data:
                # get origin country query
                origin_countryfull = form.origin_country.data
                origin_country = origin_countryfull.numericcode
            else:
                origin_country = 0

            # get destination 1
            if form.destination1.data:
                getdest1full = form.destination1.data
                getdest1 = getdest1full.numericcode
            else:
                getdest1 = 0

            # get destination2
            if form.destination2.data:
                getdest2full = form.destination2.data
                getdest2 = getdest2full.numericcode
            else:
                getdest2 = 0

            # getdestination 3
            if form.destination3.data:
                getdest3full = form.destination3.data
                getdest3 = getdest3full.numericcode
            else:
                getdest3 = 0

            # getdestination 4
            if form.destination4.data:
                getdest4full = form.destination4.data
                getdest4 = getdest4full.numericcode
            else:
                getdest4 = 0

            # getdestination 5
            if form.destination5.data:
                getdest5full = form.destination5.data
                getdest5 = getdest5full.numericcode
            else:
                getdest5 = 0

            # get get not shipping 1
            if form.not_shipping_1.data:
                getnotship1full = form.not_shipping_1.data
                getnotship1 = getnotship1full.value
            else:
                getnotship1 = 0

            # get get not shipping 2
            if form.not_shipping_2.data:
                getnotship2full = form.not_shipping_2.data
                getnotship2 = getnotship2full.value
            else:
                getnotship2 = 0

            # get get not shipping 3
            if form.not_shipping_3.data:
                getnotship3full = form.not_shipping_3.data
                getnotship3 = getnotship3full.value
            else:
                getnotship3 = 0

            # get get not shipping 4
            if form.not_shipping_1.data:
                getnotship4full = form.not_shipping_1.data
                getnotship4 = getnotship4full.value
            else:
                getnotship4 = 0

            # get get not shipping 5
            if form.not_shipping_5.data:
                getnotship5full = form.not_shipping_5.data
                getnotship5 = getnotship5full.value
            else:
                getnotship5 = 0

            # get get not shipping 6
            if form.not_shipping_6.data:
                getnotship6full = form.not_shipping_6.data
                getnotship6 = getnotship6full.value
            else:
                getnotship6 = 0

            # get shippindayleast 0
            if form.shipping_day_least_0.data:
                getshipdayleastfull0 = form.shipping_day_least_0.data
                getshipdayleast0 = getshipdayleastfull0.value
            else:
                getshipdayleast0 = 0

            # get shipping day most 0
            if form.shipping_day_most_0.data:
                getshippingdaymostfull0 = form.shipping_day_most_0.data
                getshipping_day_most0 = getshippingdaymostfull0.value
            else:
                getshipping_day_most0 = 0

            # get shippindayleast 2
            if form.shipping_day_least_2.data:
                getshipdayleastfull2 = form.shipping_day_least_2.data
                getshipdayleast2 = getshipdayleastfull2.value
            else:
                getshipdayleast2 = 0

            # get shipping day most 2
            if form.shipping_day_most_2.data:
                getshippingdaymostfull2 = form.shipping_day_most_2.data
                getshipping_day_most_2 = getshippingdaymostfull2.value
            else:
                getshipping_day_most_2 = 0

            # get shippindayleast 3
            if form.shipping_day_least_3.data:
                getshipdayleastfull3 = form.shipping_day_least_3.data
                getshipdayleast3 = getshipdayleastfull3.value
            else:
                getshipdayleast3 = 0

            # get shipping day most 3
            if form.shipping_day_most_3.data:
                getshippingdaymostfull3 = form.shipping_day_most_3.data
                getshipping_day_most_3 = getshippingdaymostfull3.value
            else:
                getshipping_day_most_3 = 0

            item.return_allowed = form.return_this_item.data
            item.shipping_free = form.shipping_free.data
            item.shipping_two = form.shipping_two.data
            item.shipping_three = form.shipping_three.data
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
            item.origin_country = origin_country
            item.destination_country_one = getdest1
            item.destination_country_two = getdest2
            item.destination_country_three = getdest3
            item.destination_country_four = getdest4
            item.destination_country_five = getdest5

            # convert image sizes
            db.session.add(item)
            db.session.commit()

            flash("Created New Item ", category="success")
            return redirect(url_for('vendorcreate.itemsforSale', itemid=item.id))
        else:
            flash(form.errors)
            return redirect(url_for('vendorcreateitem.create_item_shipping', itemid=item.id))
    return render_template('/vendor/create_item/item_shipping.html', form=form)
