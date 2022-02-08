from flask import render_template, \
    redirect, \
    url_for, \
    flash, \
    request
from flask_login import current_user
from app.promote import promote
from app import db
from app.common.decorators import \
    login_required, \
    website_offline, \
    vendoraccount_required

# models
from app.classes.item import marketItem
from app.classes.wallet_bch import BchWallet
# End Models

# forms
from app.promote.forms import \
    add_promo_form_factory, \
    PromoHomeForm
# end forms

from app.wallet_bch.wallet_btccash_work import sendcoinforad

# general imports
from datetime import datetime
from decimal import Decimal

from app.common.functions import btc_cash_convertlocaltobtc


@promote.route('/', methods=['GET', 'POST'])
@website_offline
def promotehome():
    form = PromoHomeForm()

    items = db.session\
        .query(marketItem)\
        .filter(marketItem.vendor_id == current_user.id, marketItem.aditem == 1)\
        .all()
    if request.method == 'POST':
        if form.submitcheckbox.data and form.validate_on_submit():
            for v in request.form.getlist('checkit'):
                intv = int(v)
                specific_item = db.session\
                    .query(marketItem)\
                    .filter_by(id=intv)\
                    .first()
                if specific_item.aditem == 1:
                    specific_item.aditem = 0
                    specific_item.aditem_level = 0
                    db.session.add(specific_item)
            db.session.commit()
            return redirect(url_for('promote.promotehome'))

    return render_template('/promote/home.html',
                           items=items,
                           form=form,
                           )


@promote.route('/<int:itemid>', methods=['GET', 'POST'])
@website_offline
@login_required
@vendoraccount_required
def promoteitem(itemid):
    now = datetime.utcnow()
    item = db.session\
        .query(marketItem)\
        .filter(marketItem.id == itemid)\
        .first()

    catcost = btc_cash_convertlocaltobtc(amount=1, currency=1)
    frontpagecost = btc_cash_convertlocaltobtc(amount=10, currency=1)

    decimaldollar = Decimal(catcost)
    decimaltendollar = Decimal(frontpagecost)

    if item.vendor_id == current_user.id:
        userwallet = db.session\
            .query(BchWallet)\
            .filter_by(user_id=current_user.id)\
            .first()
        useramount = userwallet.currentbalance

        myaccountform = add_promo_form_factory(item=itemid)

        form = myaccountform(
            promotype=item.aditem_level,
        )

        if request.method == 'POST':
            if form.submit.data and form.validate_on_submit():
                selection = form.promotype.data
                promoselection = selection.value
                if item.aditem == 0:
                    if promoselection == 0:
                        flash("No selection made", category="danger")
                        return redirect(url_for('promote.promoteitem', itemid=itemid))
                    elif promoselection == 1:
                        # category promo
                        if useramount > decimaldollar:
                            sendcoinforad(amount=decimaldollar,
                                          comment=item.id,
                                          user_id=current_user.id
                                          )
                            item.aditem = 1
                            item.aditem_level = 1
                            item.aditem_timer = now

                            db.session.add(item)
                            db.session.commit()

                            flash("Item Promoted", category="success")
                            return redirect(url_for('vendorcreate.itemsforSale'))
                        else:
                            flash("Not enough coin in your wallet",
                                  category="danger")
                            return redirect(url_for('promote.promoteitem', itemid=itemid))
                    elif promoselection == 2:
                        # Font page promo
                        if useramount > decimaltendollar:
                            sendcoinforad(amount=decimaltendollar,
                                          comment=item.id,
                                          user_id=current_user.id
                                          )
                            item.aditem = 1
                            item.aditem_level = 2
                            item.aditem_timer = now

                            db.session.add(item)
                            db.session.commit()

                            flash("Item Promoted", category="success")
                            return redirect(url_for('vendorcreate.itemsforSale'))
                        else:
                            flash("Not enough coin in your wallet",
                                  category="danger")
                            return redirect(url_for('promote.promoteitem', itemid=itemid))
                    else:
                        flash("Unknown Selection", category="danger")
                        return redirect(url_for('promote.promoteitem', itemid=itemid))
                else:
                    flash("Item is already promoted", category="danger")
                    return redirect(url_for('promote.promoteitem', itemid=itemid))

    else:
        return redirect(url_for('index'))

    return render_template('/promote/item.html',
                           form=form,
                           item=item,
                           catcost=catcost,
                           frontpagecost=frontpagecost
                           )
