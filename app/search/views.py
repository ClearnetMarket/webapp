from flask import render_template, request, redirect, url_for
from app.search import search
from app import db

from app.search.forms import searchForm, sortResults
from flask_paginate import Pagination, get_page_args

from app.classes.auth import Auth_User

from app.classes.item import Item_MarketItem

from flask_login import current_user
from app.search.searchfunction import headerfunctions
from sqlalchemy import or_
from app.common.decorators import website_offline


@search.route('/search=?<int:function>/<string:searchterm>', methods=['GET', 'POST'])
@website_offline
def search_master(searchterm, function):
    """
    The function is used to show search results from different keywords.
    """
    # Pagination
    search = False
    page, per_page, offset = get_page_args()
    inner_window = 2
    outer_window = 2
    # ENd Pagination

    # forms
    formsearch = searchForm()
    sortresults = sortResults(request.form)

    # get updated search term if they searched on search page
    if formsearch.searchString.data is not None:
        searchterm = formsearch.searchString.data
    else:
        searchterm = searchterm

    # vendor bar
    user, \
        order, \
        tot, \
        issues, \
        getnotifications, \
        allmsgcount, \
        userbalance, \
        unconfirmed, \
        customerdisputes = headerfunctions()
    # End Top forms bar

    # get list of results
    itemsalreadyfoundinsearchresults = []

    # Form Variables
    lowprice = sortresults.pricelow.data
    highprice = sortresults.pricehigh.data
    if lowprice == 0 and highprice == 0:
        lowprice = None
    if highprice == 0:
        highprice = None

    btc_boolean = sortresults.btc.data
    btccash_boolean = sortresults.btccash.data
    shipping_boolean = sortresults.freeshipping.data

    if btccash_boolean is False:
        btccash_sort = 0
    else:
        btccash_sort = 1

    if btc_boolean is False:
        btc_sort = 0
    else:
        btc_sort = 1

    if shipping_boolean is False:
        shipping_sort = 0
    else:
        shipping_sort = 1


    if current_user.is_authenticated:
        user = db.session.query(Auth_User).filter_by(
            username=current_user.username).first()
        # if they didnt type in anything bring the main category
        if type(searchterm) is int:
            if int(searchterm) == int(function) and int(function) != 0:
                data = db.session.query(Item_MarketItem)
                data = data.filter(Item_MarketItem.online == 1)
                data = data.filter(Item_MarketItem.category_id_0 == function)
                items = data.limit(per_page).offset(offset)
                limitdata = 0
                searchterm = ''
                pagination = Pagination(page=page,
                                        total=data.count(),
                                        search=search,
                                        record_name='items',
                                        offset=offset,
                                        per_page=per_page,
                                        css_framework='bootstrap4',
                                        inner_window=inner_window,
                                        outer_window=outer_window)
            else:
                return redirect(url_for('index'))

        else:
            searchterm = searchterm.lower()
            # if user signed in..didnt pick a category
            if function == 0:
                data = db.session\
                    .query(Item_MarketItem)\
                    .filter(Item_MarketItem.currency == user.currency).filter(Item_MarketItem.online == 1)\
                    .filter(or_(Item_MarketItem.keywords.like('%' + searchterm + '%'),
                                (Item_MarketItem.item_title.like('%' + searchterm + '%'))))

                # FILTERS
                # Price Filter
                if lowprice is None and highprice is None \
                        or lowprice is None and highprice is not None \
                        or highprice is None and lowprice is not None:
                    data = data

                else:
                    data = data.filter(lowprice <= Item_MarketItem.price)
                    data = data.filter(Item_MarketItem.price <= highprice)

                # btc cash Filter
                if btccash_sort == 0:
                    data = data
                elif btccash_sort == 1:
                    data = data.filter(Item_MarketItem.digital_currency_3 == 1)
                else:
                    data = data

                # btc Filter
                if btc_sort == 0:
                    data = data
                elif btc_sort == 1:
                    data = data.filter(Item_MarketItem.digital_currency_2 == 1)
                else:
                    data = data

                # shipping Filter
                if shipping_boolean == 0:
                    data = data
                elif shipping_boolean == 1:
                    data = data.filter(Item_MarketItem.shipping_free == 1)
                else:
                    data = data
                # END FILTERS
                total = data.count()

                # if less than ten results showed up
                if total < 10:

                    items = data.all()
                    # get a list of results so we dont show duplicate search results
                    for f in items:
                        itemsalreadyfoundinsearchresults.append(f.id)
                    # convert list to string
                    intlist = [str(x)
                               for x in itemsalreadyfoundinsearchresults]
                    # end list

                    otherdata = db.session.query(Item_MarketItem)
                    otherdata = otherdata.filter(Item_MarketItem.online == 1)

                    # FILTERS
                    # Price Filter
                    if lowprice is None and highprice is None \
                            or lowprice is None and highprice is not None \
                            or highprice is None and lowprice is not None:
                        otherdata = otherdata
                    else:
                        otherdata = otherdata.filter(
                            lowprice <= Item_MarketItem.price)
                        otherdata = otherdata.filter(
                            Item_MarketItem.price <= highprice)

                    # btc cash Filter
                    if btccash_sort == 0:
                        otherdata = otherdata
                    elif btccash_sort == 1:
                        otherdata = otherdata.filter(
                            Item_MarketItem.digital_currency_3 == 1)
                    else:
                        otherdata = otherdata

                    # btc Filter
                    if btc_sort == 0:
                        otherdata = otherdata
                    elif btc_sort == 1:
                        otherdata = otherdata.filter(
                            Item_MarketItem.digital_currency_2 == 1)
                    else:
                        otherdata = otherdata

                    # shipping Filter
                    if shipping_boolean == 0:
                        otherdata = otherdata
                    elif shipping_boolean == 1:
                        otherdata = otherdata.filter(
                            Item_MarketItem.shipping_free == 1)
                    else:
                        otherdata = otherdata

                    # END FILTERS
                    otherdata = otherdata.filter(
                        (~Item_MarketItem.id.in_(intlist)))
                    limitdata = otherdata.limit(10)

                # got more than 10 results
                else:
                    items = data.limit(per_page).offset(offset)
                    # dont add extra results
                    limitdata = 0

                pagination = Pagination(page=page,
                                        total=data.count(),
                                        search=search,
                                        record_name='items',
                                        offset=offset,
                                        per_page=per_page,
                                        css_framework='bootstrap4',
                                        inner_window=inner_window,
                                        outer_window=outer_window)

            # user signed in..picked something specific with searchterm
            else:
                data = db.session\
                    .query(Item_MarketItem)\
                    .filter(Item_MarketItem.currency == user.currency)\
                    .filter(Item_MarketItem.online == 1)\
                    .filter(Item_MarketItem.image_one != '0')\
                    .filter(Item_MarketItem.category_id_0 == function)\
                    .filter(or_(Item_MarketItem.keywords.like('%' + searchterm + '%'),
                                (Item_MarketItem.item_title.like('%' + searchterm + '%'))))\
                    .filter(or_(Item_MarketItem.destination_country_one == user.country,
                            Item_MarketItem.destination_country_two == user.country,
                            Item_MarketItem.destination_country_three == user.country,
                            Item_MarketItem.destination_country_four == user.country,
                            Item_MarketItem.destination_country_five == user.country))

                # FILTERS
                # Price Filter
                if lowprice is None and highprice is None \
                        or lowprice is None and highprice is not None \
                        or highprice is None and lowprice is not None:
                    data = data

                else:
                    data = data.filter(lowprice <= Item_MarketItem.price)
                    data = data.filter(Item_MarketItem.price <= highprice)

                # btc cash Filter
                if btccash_sort == 0:
                    data = data
                elif btccash_sort == 1:
                    data = data.filter(Item_MarketItem.digital_currency_3 == 1)
                else:
                    data = data

                # btc Filter
                if btc_sort == 0:
                    data = data
                elif btc_sort == 1:
                    data = data.filter(Item_MarketItem.digital_currency_2 == 1)
                else:
                    data = data

                # shipping Filter
                if shipping_boolean == 0:
                    data = data
                elif shipping_boolean == 1:
                    data = data.filter(Item_MarketItem.shipping_free == 1)
                else:
                    data = data
                # END FILTERS

                total = data.count()
                # if less than ten results, query more data

                if total < 10:
                    items = data.all()
                    # get a list of results so we dont show duplicate search results
                    for f in items:
                        itemsalreadyfoundinsearchresults.append(f.id)
                    # convert list to string
                    intlist = [str(x)
                               for x in itemsalreadyfoundinsearchresults]
                    # end list

                    otherdata = db.session\
                        .query(Item_MarketItem)\
                        .filter(Item_MarketItem.image_one != '0')\
                        .filter_by(currency=user.currency)\
                        .filter(Item_MarketItem.online == 1)\
                        .filter(or_(Item_MarketItem.destination_country_one == user.country,
                                Item_MarketItem.destination_country_two == user.country,
                                Item_MarketItem.destination_country_three == user.country,
                                Item_MarketItem.destination_country_four == user.country,
                                Item_MarketItem.destination_country_five == user.country))\
                        .filter((~Item_MarketItem.id.in_(intlist)))

                    # FILTERS
                    # Price Filter
                    if lowprice is None and highprice is None \
                            or lowprice is None and highprice is not None \
                            or highprice is None and lowprice is not None:
                        otherdata = otherdata

                    else:
                        otherdata = otherdata.filter(
                            lowprice <= Item_MarketItem.price)
                        otherdata = otherdata.filter(
                            Item_MarketItem.price <= highprice)

                    # btc cash Filter
                    if btccash_sort == 0:
                        otherdata = otherdata
                    elif btccash_sort == 1:
                        otherdata = otherdata.filter(
                            Item_MarketItem.digital_currency_3 == 1)
                    else:
                        otherdata = otherdata

                    # btc Filter
                    if btc_sort == 0:
                        otherdata = otherdata
                    elif btc_sort == 1:
                        otherdata = otherdata.filter(
                            Item_MarketItem.digital_currency_2 == 1)
                    else:
                        otherdata = otherdata

                    # shipping Filter
                    if shipping_boolean == 0:
                        otherdata = otherdata
                    elif shipping_boolean == 1:
                        otherdata = otherdata.filter(
                            Item_MarketItem.shipping_free == 1)
                    else:
                        otherdata = otherdata

                    # END FILTERS
                    limitdata = otherdata.limit(10)
                else:
                    items = data.limit(per_page).offset(offset)
                    # dont add extra results, just get pagination
                    limitdata = 0
                pagination = Pagination(page=page,
                                        total=data.count(),
                                        search=search,
                                        record_name='items',
                                        offset=offset,
                                        per_page=per_page,
                                        css_framework='bootstrap4',
                                        inner_window=inner_window,
                                        outer_window=outer_window)

    # NOT SIGNED IN
    else:
        user = 'Guest'
        # if they didnt type in anything bring the main category
        # in the future return to a main page
        if type(searchterm) is int:
            if int(searchterm) == int(function) and int(function) != 0:
                data = db.session\
                    .query(Item_MarketItem)\
                    .filter(Item_MarketItem.online == 1)\
                    .filter(Item_MarketItem.category_id_0 == function)\
                    .limit(per_page)\
                    .offset(offset)
                limitdata = 0

                pagination = Pagination(page=page,
                                        total=data.count(),
                                        search=search,
                                        record_name='items',
                                        offset=offset,
                                        per_page=per_page,
                                        css_framework='bootstrap4',
                                        inner_window=inner_window,
                                        outer_window=outer_window)
            else:
                return redirect(url_for('index'))
        else:
            searchterm = searchterm.lower()
            # not signed in ..if they selected nothing
            if function == 0:

                data = db.session\
                    .query(Item_MarketItem)\
                    .filter(Item_MarketItem.online == 1)\
                    .filter(or_(Item_MarketItem.keywords.like('%' + searchterm + '%'),
                                (Item_MarketItem.item_title.like('%' + searchterm + '%'))))

                # FILTERS
                # Price Filter
                if lowprice is None and highprice is None \
                        or lowprice is None and highprice is not None \
                        or highprice is None and lowprice is not None:
                    data = data

                else:
                    data = data.filter(lowprice <= Item_MarketItem.price)
                    data = data.filter(Item_MarketItem.price <= highprice)

                # btc cash Filter
                if btccash_sort == 0:
                    data = data
                elif btccash_sort == 1:
                    data = data.filter(Item_MarketItem.digital_currency_3 == 1)
                else:
                    data = data

                # btc Filter
                if btc_sort == 0:
                    data = data
                elif btc_sort == 1:
                    data = data.filter(Item_MarketItem.digital_currency_2 == 1)
                else:
                    data = data

                # shipping Filter
                if shipping_boolean == 0:
                    data = data
                elif shipping_boolean == 1:
                    data = data.filter(Item_MarketItem.shipping_free == 1)
                else:
                    data = data
                # END FILTERS

                total = data.count()
                # if not enough results, redo query and add query for all data based off online
                if total < 10:

                    items = data.all()

                    # get a list of results so we dont show duplicate search results
                    for f in items:
                        itemsalreadyfoundinsearchresults.append(f.id)
                    # convert list to string
                    intlist = [str(x)
                               for x in itemsalreadyfoundinsearchresults]
                    # end list

                    alldata = db.session\
                        .query(Item_MarketItem)\
                        .filter(Item_MarketItem.online == 1)\
                        .order_by(Item_MarketItem.item_rating.desc())\
                        .filter((~Item_MarketItem.id.in_(intlist)))

                    # FILTERS
                    # Price Filter
                    if lowprice is None and highprice is None \
                            or lowprice is None and highprice is not None \
                            or highprice is None and lowprice is not None:
                        alldata = alldata
                    else:
                        alldata = alldata.filter(
                            lowprice <= Item_MarketItem.price)
                        alldata = alldata.filter(
                            Item_MarketItem.price <= highprice)
                    # END FILTERS

                    limitdata = alldata.limit(10)

                else:
                    items = data.limit(per_page).offset(offset)
                    limitdata = 0
                pagination = Pagination(page=page,
                                        total=data.count(),
                                        search=search,
                                        record_name='items',
                                        offset=offset,
                                        per_page=per_page,
                                        css_framework='bootstrap4',
                                        inner_window=inner_window,
                                        outer_window=outer_window)

            # NOT SIGNED IN ..if they picked specific category and entered searchterm
            else:
                # Regular query if not signed in.
                data = db.session\
                    .query(Item_MarketItem)\
                    .filter(Item_MarketItem.category_id_0 == function)\
                    .filter(Item_MarketItem.online == 1)\
                    .filter(or_(Item_MarketItem.keywords.like('%' + searchterm + '%'),
                            (Item_MarketItem.item_title.like('%' + searchterm + '%'))))

                # FILTERS
                # Price Filter
                if lowprice is None and highprice is None \
                        or lowprice is None and highprice is not None \
                        or highprice is None and lowprice is not None:
                    data = data

                else:
                    data = data.filter(lowprice <= Item_MarketItem.price)
                    data = data.filter(Item_MarketItem.price <= highprice)

                # btc cash Filter
                if btccash_sort == 0:
                    data = data
                elif btccash_sort == 1:
                    data = data.filter(Item_MarketItem.digital_currency_3 == 1)
                else:
                    data = data

                # btc Filter
                if btc_sort == 0:
                    data = data
                elif btc_sort == 1:
                    data = data.filter(Item_MarketItem.digital_currency_2 == 1)
                else:
                    data = data

                # shipping Filter
                if shipping_boolean == 0:
                    data = data
                elif shipping_boolean == 1:
                    data = data.filter(Item_MarketItem.shipping_free == 1)
                else:
                    data = data
                # END FILTERS

                total = data.count()

                # if didnt return enough results
                if total < 10:
                    items = data.all()
                    # get a list of results so we dont show duplicate search results
                    for f in items:
                        itemsalreadyfoundinsearchresults.append(f.id)
                    # convert list to string
                    intlist = [str(x)
                               for x in itemsalreadyfoundinsearchresults]
                    # end list
                    alldata = db.session\
                        .query(Item_MarketItem)\
                        .filter(Item_MarketItem.online == 1)\
                        .order_by(Item_MarketItem.item_rating.desc())\
                        .filter((~Item_MarketItem.id.in_(intlist)))
                    # FILTERS
                    # Price Filter
                    if lowprice is None and highprice is None \
                            or lowprice is None and highprice is not None \
                            or highprice is None and lowprice is not None:
                        alldata = alldata

                    else:
                        alldata = alldata.filter(
                            lowprice <= Item_MarketItem.price)
                        alldata = alldata.filter(
                            Item_MarketItem.price <= highprice)

                    # btc cash Filter
                    if btccash_sort == 0:
                        alldata = alldata
                    elif btccash_sort == 1:
                        alldata = alldata.filter(
                            Item_MarketItem.digital_currency_3 == 1)
                    else:
                        alldata = alldata

                    # btc Filter
                    if btc_sort == 0:
                        alldata = alldata
                    elif btc_sort == 1:
                        alldata = alldata.filter(
                            Item_MarketItem.digital_currency_2 == 1)
                    else:
                        alldata = alldata

                    # shipping Filter
                    if shipping_boolean == 0:
                        alldata = alldata
                    elif shipping_boolean == 1:
                        alldata = alldata.filter(
                            Item_MarketItem.shipping_free == 1)
                    else:
                        alldata = alldata
                    # END FILTERS
                    limitdata = alldata.limit(10)

                # use the query origonally
                else:
                    items = data.limit(10)
                    limitdata = 0

                pagination = Pagination(page=page,
                                        total=data.count(),
                                        search=search,
                                        record_name='items',
                                        offset=offset,
                                        per_page=per_page,
                                        css_framework='bootstrap4',
                                        inner_window=inner_window,
                                        outer_window=outer_window)

    if request.method == 'POST':

        if sortresults.sort.data:

            # cats
            categoryfull = formsearch.category.data
            cat = categoryfull.id
            formfunction = cat
            # Prices
            lowprice = sortresults.pricelow.data
            highprice = sortresults.pricehigh.data

            # catch dynamic variables
            if formsearch.searchString.data == '' and cat == 0:
                return redirect(url_for('index'))

            if formsearch.searchString.data == '':
                formsearch.searchString.data = cat

            if lowprice == 0 and highprice == 0:
                lowprice = None

            if highprice == 0:
                highprice = None
            # currency sorting
            btc_boolean = sortresults.btc.data
            btccash_boolean = sortresults.btccash.data
            shipping_boolean = sortresults.freeshipping.data
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

            return render_template('search/searchresult.html',
                                   # forms
                                   form=formsearch,
                                   # header stuff
                                   user=user,
                                   order=order,
                                   tot=tot,
                                   issues=issues,
                                   getnotifications=getnotifications,
                                   allmsgcount=allmsgcount,
                                   customerdisputes=customerdisputes,
                                   userbalance=userbalance,
                                   unconfirmed=unconfirmed,
                                   # pagination
                                   pagination=pagination,
                                   items=items,
                                   limitdata=limitdata,
                                   sortresults=sortresults,
                                   # form variables
                                   searchterm=formsearch.searchString.data,
                                   function=formfunction,
                                   lowprice=lowprice,
                                   highprice=highprice,
                                   btccash_sort=btccash_sort,
                                   btc_sort=btc_sort,
                                   shipping_sort=shipping_sort,
                                   )
        if formsearch.validate_on_submit():

            # cats
            categoryfull = formsearch.category.data
            cat = categoryfull.id

            if formsearch.searchString.data == '' and cat == 0:
                return redirect(url_for('index'))

            if formsearch.searchString.data == '':
                formsearch.searchString.data = cat

            return redirect(url_for('search.search_master',
                                    searchterm=formsearch.searchString.data,
                                    function=cat,
                                    ))

    return render_template('search/searchresult.html',
                           # forms
                           form=formsearch,
                           # header stuff
                           user=user,
                           order=order,
                           tot=tot,
                           issues=issues,
                           getnotifications=getnotifications,
                           allmsgcount=allmsgcount,
                           customerdisputes=customerdisputes,
                           userbalance=userbalance,
                           unconfirmed=unconfirmed,
                           # pagination
                           pagination=pagination,
                           items=items,
                           limitdata=limitdata,
                           sortresults=sortresults,
                           # form variables
                           searchterm=searchterm,
                           function=function,
                           lowprice=lowprice,
                           highprice=highprice,
                           btccash_sort=btccash_sort,
                           btc_sort=btc_sort,
                           shipping_sort=shipping_sort,
                           )
