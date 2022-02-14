from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.promote import promote
from app import db
from decimal import Decimal
from datetime import datetime
from app.common.decorators import \
    login_required, \
    website_offline, \
    vendoraccount_required
from app.common.functions import convert_local_to_bch

# models
from app.classes.item import Item_MarketItem
from app.classes.wallet_bch import Bch_Wallet
# End Models

# forms
from app.promote.forms import \
    add_promo_form_factory, \
    PromoHomeForm
# end forms

from app.wallet_bch.wallet_btccash_work import sendcoinforad

# general imports



@promote.route('/', methods=['GET', 'POST'])
@website_offline
def promote_home():
    form = PromoHomeForm()

    items = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.vendor_id == current_user.id, Item_MarketItem.ad_item is True)\
        .all()
    if request.method == 'POST':
        if form.submitcheckbox.data and form.validate_on_submit():
            for v in request.form.getlist('checkit'):
                intv = int(v)
                specific_item = db.session\
                    .query(Item_MarketItem)\
                    .filter_by(id=intv)\
                    .first()
                if specific_item.ad_item is True:
                    specific_item.ad_item = 0
                    specific_item.ad_item_level = 0
                    db.session.add(specific_item)
            db.session.commit()
            return redirect(url_for('promote.promote_home'))

    return render_template('/promote/home.html',
                           items=items,
                           form=form,
                           )


@promote.route('/<int:itemid>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def promote_item(itemid):
    now = datetime.utcnow()
    item = db.session\
        .query(Item_MarketItem)\
        .filter(Item_MarketItem.id == itemid)\
        .first()

    catcost = convert_local_to_bch(amount=1, currency=1)
    frontpagecost = convert_local_to_bch(amount=10, currency=1)

    decimaldollar = Decimal(catcost)
    decimaltendollar = Decimal(frontpagecost)

    if item.vendor_id == current_user.id:
        userwallet = db.session\
            .query(Bch_Wallet)\
            .filter_by(user_id=current_user.id)\
            .first()
        useramount = userwallet.currentbalance

        myaccountform = add_promo_form_factory(item=itemid)

        form = myaccountform(
            promotype=item.ad_item_level,
        )

        if request.method == 'POST':
            if form.submit.data and form.validate_on_submit():
                selection = form.promotype.data
                promoselection = selection.value
                if item.ad_item == 0:
                    if promoselection == 0:
                        flash("No selection made", category="danger")
                        return redirect(url_for('promote.promote_item', itemid=itemid))
                    elif promoselection == 1:
                        # category promo
                        if useramount > decimaldollar:
                            sendcoinforad(amount=decimaldollar,
                                          comment=item.id,
                                          user_id=current_user.id
                                          )
                            item.ad_item = 1
                            item.ad_item_level = 1
                            item.ad_item_timer = now

                            db.session.add(item)
                            db.session.commit()

                            flash("Item Promoted", category="success")
                            return redirect(url_for('vendorcreate.vendorcreate_items_for_sale'))
                        else:
                            flash("Not enough coin in your wallet",
                                  category="danger")
                            return redirect(url_for('promote.promote_item', itemid=itemid))
                    elif promoselection == 2:
                        # Font page promo
                        if useramount > decimaltendollar:
                            sendcoinforad(amount=decimaltendollar,
                                          comment=item.id,
                                          user_id=current_user.id
                                          )
                            item.ad_item = 1
                            item.ad_item_level = 2
                            item.ad_item_timer = now

                            db.session.add(item)
                            db.session.commit()

                            flash("Item Promoted", category="success")
                            return redirect(url_for('vendorcreate.vendorcreate_items_for_sale'))
                        else:
                            flash("Not enough coin in your wallet",
                                  category="danger")
                            return redirect(url_for('promote.promote_item', itemid=itemid))
                    else:
                        flash("Unknown Selection", category="danger")
                        return redirect(url_for('promote.promote_item', itemid=itemid))
                else:
                    flash("Item is already promoted", category="danger")
                    return redirect(url_for('promote.promote_item', itemid=itemid))

    else:
        return redirect(url_for('index'))

    return render_template('/promote/item.html',
                           form=form,
                           item=item,
                           catcost=catcost,
                           frontpagecost=frontpagecost
                           )
