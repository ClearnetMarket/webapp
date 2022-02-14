from flask import render_template, redirect, url_for, request, flash
from sqlalchemy import or_
from flask_paginate import\
    Pagination,\
    get_page_args
from app.category import category
from app import db
# models
from app.classes.item import Item_MarketItem
from app.classes.wallet_bch import Bch_Prices
from app.classes.category import Category_Categories
# end models
from app.search.forms import\
    searchForm,\
    sortResults
from app.search.searchfunction import\
    headerfunctions
from datetime import\
    datetime
from app.common.decorators import \
    website_offline


@category.route('/category/<int:maincatid>', methods=['GET', 'POST'])
@website_offline
def view_category(maincatid):
    now = datetime.utcnow()
    # forms
    formsearch = searchForm()
    sortresults = sortResults(request.form)

    # Top Bar
    user, \
        order, \
        tot, \
        issues, \
        getnotifications, \
        allmsgcount, \
        userbalance, \
        unconfirmed, \
        customerdisputes = headerfunctions()
    get_cats = db.session\
        .query(Category_Categories)\
        .filter(Category_Categories.id != 1000, Category_Categories.id != 0)\
        .order_by(Category_Categories.name.asc())\
        .all()
    # Currency Prices
    try:
        btc_cash_price = db.session\
            .query(Bch_Prices)\
            .filter(or_(Bch_Prices.currency_id == 1,
                        Bch_Prices.currency_id == 30,
                        Bch_Prices.currency_id == 17,
                        Bch_Prices.currency_id == 23,
                        Bch_Prices.currency_id == 30,
                        Bch_Prices.currency_id == 6,
                        Bch_Prices.currency_id == 4,
                        ))\
            .order_by(Bch_Prices.currency_id.asc())\
            .all()
    except Exception as e:
        btc_cash_price = 0
    # Currency Prices

    # Pagination
    search = False
    q = request.args.get('q')
    if q:
        search = True
    page, per_page, offset = get_page_args()
    inner_window = 1  # search bar at bottom used for .. lots of pages
    outer_window = 1  # search bar at bottom used for .. lots of pages
    per_page = 10  # how many items per page
    # End Pagination

    # Side Sort
    lowprice = None
    highprice = None
    btccash_sort = None
    btc_sort = None
    shipping_sort = None
    # End side sort

    # PROMOTED
    promoteditems = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.online == 1)\
        .filter(Item_MarketItem.ad_item is True)\
        .filter(Item_MarketItem.ad_item_level == 1)\
        .order_by(Item_MarketItem.total_sold.desc())\
        .limit(4)
    # END PROMOTED

    # get the category
    getcategory = db.session\
        .query(Category_Categories)\
        .filter(Category_Categories.id == maincatid)\
        .first()
    g = db.session
    # Main Page search
    try:
        itemfull = db.session\
            .query(Item_MarketItem)\
            .filter(Item_MarketItem.online == 1)\
            .filter(Item_MarketItem.category_id_0 == maincatid)\
            .limit(per_page).offset(offset)

        pagination = Pagination(page=page,
                                total=itemfull.count(),
                                search=search,
                                record_name='items',
                                offset=offset,
                                per_page=per_page,
                                css_framework='bootstrap',
                                inner_window=inner_window,
                                outer_window=outer_window)

    except Exception as e:
        return redirect(url_for('index'))
    # END Main Page search
    itemquery = None

    # Forms
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

        if sortresults.sort.data:
            # form variables here
            lowprice = sortresults.pricelow.data
            highprice = sortresults.pricehigh.data
            if lowprice == 0 and highprice == 0:
                lowprice = None
            elif highprice == 0:
                highprice = None
                lowprice = None
            elif lowprice == 0 and highprice != 0:
                highprice = highprice
                lowprice = 0
            else:
                pass
            # currency sorting
            btc_boolean = formsearch.btc.data
            btccash_boolean = formsearch.btccash.data
            shipping_boolean = formsearch.freeshipping.data

            if btccash_boolean is False:
                btccash_sort = 0
            else:
                btccash_sort = 1

            if btc_boolean is False:
                btc_sort = 0
            else:
                btc_sort = 1

            # shipping sorting
            if shipping_boolean is False:
                shipping_sort = 0
            else:
                shipping_sort = 1

            ###
            # Most relevant
            ##

            itemfull = db.session\
                .query(Item_MarketItem)\
                .filter(Item_MarketItem.online == 1)

            # FILTERS
            # Price Filter
            if lowprice is None and highprice is None \
                    or lowprice is None and highprice is not None \
                    or highprice is None and lowprice is not None:
                itemfull = itemfull

            else:
                itemfull = itemfull.filter(lowprice <= Item_MarketItem.price)\
                    .filter(Item_MarketItem.price <= highprice)

            # btc Filter
            if btc_sort == 0:
                itemfull = itemfull
            elif btc_sort == 1:
                itemfull = itemfull.filter(
                    Item_MarketItem.digital_currency_2 == 1)
            else:
                itemfull = itemfull

            # btc cash Filter
            if btccash_sort == 0:
                itemfull = itemfull
            elif btccash_sort == 1:
                itemfull = itemfull.filter(
                    Item_MarketItem.digital_currency_3 == 1)
            else:
                itemfull = itemfull

            # shipping Filter
            if shipping_boolean == 0:
                itemfull = itemfull
            elif shipping_boolean == 1:
                itemfull = itemfull.filter(Item_MarketItem.shipping_free == 1)
            else:
                itemfull = itemfull
            # END FILTERS

            # No sort
            if sortresults.sortCategory.data == '0':
                itemfull = itemfull
            ###
            # PRICE highest first
            ##
            elif sortresults.sortCategory.data == '1':
                itemfull = itemfull.order_by(Item_MarketItem.price.desc())
            ###
            # PRICE lowest first
            ##
            elif sortresults.sortCategory.data == '2':
                itemfull = itemfull.order_by(Item_MarketItem.price.asc())

            ###
            # top selling/traded
            ##
            elif sortresults.sortCategory.data == '3':
                itemfull = itemfull.order_by(Item_MarketItem.total_sold.desc())

            else:
                flash(sortresults.sortCategory.data, category="danger")
                itemfull = itemfull

            itemquery = itemfull.limit(per_page).offset(offset)

            pagination = Pagination(page=page,
                                    total=itemfull.count(),
                                    search=search,
                                    record_name='items',
                                    offset=offset,
                                    per_page=per_page,
                                    css_framework='bootstrap4',
                                    inner_window=inner_window,
                                    outer_window=outer_window)

        return render_template('/search/categories/viewcategory.html',

                               # forms
                               form=formsearch,

                               # header stuff
                               get_cats=get_cats,
                               user=user,
                               now=now,
                               order=order,
                               tot=tot,
                               issues=issues,
                               getnotifications=getnotifications,
                               allmsgcount=allmsgcount,
                               userbalance=userbalance,
                               unconfirmed=unconfirmed,
                               customerdisputes=customerdisputes,

                               # page specific
                               maincatid=maincatid,
                               itemquery=itemquery,
                               sortresults=sortresults,
                               pagination=pagination,
                               getcategory=getcategory,

                               # side
                               highprice=highprice,
                               lowprice=lowprice,
                               btccash_sort=btccash_sort,
                               btc_sort=btc_sort,
                               shipping_sort=shipping_sort,

                               # promotions
                               promoteditems=promoteditems,

                               # coin prices

                               btc_cash_price=btc_cash_price,

                               )

    return render_template('/search/categories/viewcategory.html',
                           # forms
                           form=formsearch,
                           # header stuff
                           user=user,
                           get_cats=get_cats,
                           now=now,
                           order=order,
                           tot=tot,
                           issues=issues,
                           getnotifications=getnotifications,
                           allmsgcount=allmsgcount,
                           userbalance=userbalance,
                           unconfirmed=unconfirmed,
                           customerdisputes=customerdisputes,
                           # page specific
                           maincatid=maincatid,
                           itemquery=itemquery,
                           sortresults=sortresults,
                           pagination=pagination,
                           getcategory=getcategory,
                           # side
                           highprice=highprice,
                           lowprice=lowprice,
                           # promotions
                           promoteditems=promoteditems,
                           # coin prices
                           btc_cash_price=btc_cash_price
                           )
