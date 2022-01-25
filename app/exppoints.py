
# type 1 = user bought
# type 2 = review vendor gave
# type 3 = review_user gave
# type 4 = feedback
# type 5 = bonus finishing early
# type 6 =user recieved
# type 7 = vendor recieved
# type 8 = user cancelled
# type 9 = vendor cancelled
# type 10 = user return
# type 11 = vendor sold
# type 15= bitcoin trade


standardpricefactor = 1000
standardpricefactor_btc = 5000
points_trade = 10
points_sale = 25
points_feedback = 100
points_review = 10
points_recieveditem = 10
points_usercancel = -50
points_vendorcancel = -25
points_return = -75
btcbonus = 0
digbonus = 5
itembonus = 0


def exppoint(user, price, type, quantity, currency):
    from app import db
    from app.classes.profile import exptable
    from app.classes.achievements import UserAchievements
    from app.common.functions import btc_cash_convertlocaltobtc, btc_cash_converttolocal
    from decimal import Decimal
    from datetime import datetime
    from app.achievements.e import levelawards

    now = datetime.utcnow()
    # get current user stats
    getuser = db.session.query(UserAchievements)
    getuser = getuser.filter(UserAchievements.userid == user)
    guser = getuser.first()
    # current user points

    currentPoints = guser.experiencepoints
    if 1 <= guser.level <= 3:
        experienceperlevel = 300
    elif 4 <= guser.level <= 7:
        experienceperlevel = 500
    elif 8 <= guser.level <= 10:
        experienceperlevel = 1000
    elif 11 <= guser.level <= 14:
        experienceperlevel = 1500
    elif 16 <= guser.level <= 20:
        experienceperlevel = 2000
    elif 21 <= guser.level <= 25:
        experienceperlevel = 2250
    elif 26 <= guser.level <= 30:
        experienceperlevel = 5500
    elif 26 <= guser.level <= 30:
        experienceperlevel = 10000
    elif 26 <= guser.level <= 30:
        experienceperlevel = 15000
    elif 30 <= guser.level <= 50:
        experienceperlevel = 20000
    elif 51 <= guser.level <= 100:
        experienceperlevel = 25000
    else:
        experienceperlevel = 1000


    # get user exp table
    if currency == 0:
        # convert btc to usd
        y = btc_cash_converttolocal(amount=price, currency=1)
    elif currency == 1:
        # no converting
        y = price
    else:
        # convert to btc then to usd
        x = btc_cash_convertlocaltobtc(amount=price, currency=currency)
        # convert to usd
        y = btc_cash_converttolocal(amount=Decimal(x), currency=1)

    # If they sold or bought something
    if type == 1:
        def percentage(percent, whole):
            c = ((Decimal(percent) / Decimal(whole)) * 100)
            return int(Decimal(c))

        # adds more if they spent more
        def bonus(percent):
            if 0 == int(percent):
                bonuspercent = 1
            elif 1 <= int(percent) <= 10:
                bonuspercent = 1
            elif 10 <= int(percent) <= 25:
                bonuspercent = 5
            elif 26 <= int(percent) <= 50:
                bonuspercent = 10
            elif 51 <= int(percent) <= 75:
                bonuspercent = 25
            elif 76 <= int(percent) <= 100:
                bonuspercent = 50
            elif 100 <= int(percent) <= 125:
                bonuspercent = 75
            elif 126 <= int(percent):
                bonuspercent = 100
            else:
                bonuspercent = 0
            return bonuspercent

        amountspent = y*quantity
        percent = percentage(percent=((amountspent)), whole=standardpricefactor)
        adjusted = bonus(percent=percent)
        points = points_sale
        addpoints = int((currentPoints + points + adjusted + itembonus))
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)

        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up
        exp = int(points + adjusted + itembonus)

        exptot = exptable(
            userid=user,
            type=1,
            amount=exp,
            timestamp=now,
        )

        db.session.add(guser)
        db.session.add(exptot)

    # vendor review
    elif type == 2:
        def adjrating(quantity):
            if quantity == 1:
                adjustment = -25
                return adjustment
            if quantity == 2:
                adjustment = -10
                return adjustment
            if quantity == 3:
                adjustment = 1
                return adjustment
            if quantity == 4:
                adjustment = 10
                return adjustment
            if quantity == 5:
                adjustment = 25
                return adjustment

        adjusted = adjrating(quantity=quantity)
        addpoints = int((currentPoints + adjusted))
        exp = adjusted
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)
        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up

        exp = exptable(
            userid=user,
            type=2,
            amount=exp,
            timestamp=now,
        )
        db.session.add(guser)
        db.session.add(exp)

    # user left a review
    elif type == 3:
        # 1-5 equals review they gave
        def adjrating(quantity):
            if quantity == 1:
                adjustment = -10
                return adjustment
            if quantity == 2:
                adjustment = -5
                return adjustment
            if quantity == 3:
                adjustment = 1
                return adjustment
            if quantity == 4:
                adjustment = 5
                return adjustment
            if quantity == 5:
                adjustment = 10
                return adjustment

        adjusted =adjrating(quantity=quantity)
        addpoints = int((currentPoints + points_review + adjusted))
        exp = points_review + adjusted
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)
        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up
        exp = exptable(
            userid=user,
            type=3,
            amount=exp,
            timestamp=now,
        )
        db.session.add(guser)
        db.session.add(exp)

    # user recieved a review
    elif type == 6:
        def adjrating(quantity):
            if quantity == 1:
                adjustment = -10
                return adjustment
            if quantity == 2:
                adjustment = -5
                return adjustment
            if quantity == 3:
                adjustment = 1
                return adjustment
            if quantity == 4:
                adjustment = 5
                return adjustment
            if quantity == 5:
                adjustment = 10
                return adjustment

        adjusted = adjrating(quantity=quantity)
        addpoints = int((currentPoints + points_review + adjusted))
        exp = points_review + adjusted
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)
        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up
        db.session.add(guser)
        db.session.flush()
        if guser.experiencepoints < 0:
            guser.experiencepoints = 0
        exp = exptable(
            userid=user,
            type=6,
            amount=exp,
            timestamp=now,
        )
        db.session.add(guser)
        db.session.add(exp)

    # Vendor recieved a review
    elif type == 7:
        def adjrating(quantity):
            if quantity == 1:
                adjustment = -100
                return adjustment
            if quantity == 2:
                adjustment = -10
                return adjustment
            if quantity == 3:
                adjustment = 1
                return adjustment
            if quantity == 4:
                adjustment = 10
                return adjustment
            if quantity == 5:
                adjustment = 25
                return adjustment

        adjusted = adjrating(quantity=quantity)
        addpoints = int((currentPoints + points_review + adjusted))
        exp = points_review + adjusted
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)
        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up

        exp = exptable(
            userid=user,
            type=7,
            amount=exp,
            timestamp=now,
        )
        db.session.add(guser)
        db.session.add(exp)

    # website feedback
    elif type == 4:
        addpoints = int((currentPoints + points_feedback))
        exp = points_feedback
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)
        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up
        exp = exptable(
            userid=user,
            type=4,
            amount=exp,
            timestamp=now,
        )
        db.session.add(guser)
        db.session.add(exp)

    # Bonus marked as recieved
    elif type == 5:
        addpoints = int((currentPoints + points_recieveditem))
        exp = points_recieveditem
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)
        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up
        exp = exptable(
            userid=user,
            type=5,
            amount=exp,
            timestamp=now,
        )
        db.session.add(guser)
        db.session.add(exp)


    # user cancelled
    elif type == 8:
        addpoints = int((currentPoints + points_usercancel))
        exp = points_usercancel
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)
        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up

        exp = exptable(
            userid=user,
            type=8,
            amount=exp,
            timestamp=now,
        )
        db.session.add(guser)
        db.session.add(exp)


    # vendor cancelled
    elif type == 9:
        addpoints = int((currentPoints + points_vendorcancel))
        exp = points_vendorcancel
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)
        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up

        exp = exptable(
            userid=user,
            type=9,
            amount=exp,
            timestamp=now,
        )

        db.session.add(guser)
        db.session.add(exp)

    # user returned item
    elif type == 10:
        addpoints = int((currentPoints + points_return))
        exp = points_return
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)
        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up

        exp = exptable(
            userid=user,
            type=10,
            amount=exp,
            timestamp=now,
        )

        db.session.add(guser)
        db.session.add(exp)

    # vendor sold something
    elif type == 11:
        def percentage(percent, whole):
            c = ((Decimal(percent) / Decimal(whole)) * 100)
            return int(Decimal(c))

        # adds more if they spent more
        def bonus(percent):
            if 0 == int(percent):
                bonuspercent = 1
            elif 1 <= int(percent) <= 10:
                bonuspercent = 1
            elif 10 <= int(percent) <= 25:
                bonuspercent = 5
            elif 26 <= int(percent) <= 50:
                bonuspercent = 10
            elif 51 <= int(percent) <= 75:
                bonuspercent = 25
            elif 76 <= int(percent) <= 100:
                bonuspercent = 50
            elif 100 <= int(percent) <= 125:
                bonuspercent = 75
            elif 126 <= int(percent):
                bonuspercent = 100
            else:
                bonuspercent = 0
            return bonuspercent

        amountspent = y*quantity
        percent = percentage(percent=(amountspent), whole=standardpricefactor)
        adjusted = bonus(percent=percent)
        points = points_sale
        addpoints = int((currentPoints + points + adjusted + itembonus))
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)
        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up
        exp = int(points + adjusted + itembonus)
        exptot = exptable(
            userid=user,
            type=11,
            amount=exp,
            timestamp=now,
        )
        db.session.add(guser)
        db.session.add(exptot)

    # bitcoin trade customer
    elif type == 15:
        def percentage(percent, whole):
            c = ((Decimal(percent) / Decimal(whole)) * 100)
            return int(Decimal(c))

        # adds more if they spent more
        def bonus(percent):
            if 0 == int(percent):
                bonuspercent = 1
            elif 1 <= int(percent) <= 10:
                bonuspercent = 1
            elif 10 <= int(percent) <= 25:
                bonuspercent = 15
            elif 26 <= int(percent) <= 50:
                bonuspercent = 25
            elif 51 <= int(percent) <= 75:
                bonuspercent = 50
            elif 76 <= int(percent) <= 100:
                bonuspercent = 100
            elif 100 <= int(percent) <= 125:
                bonuspercent = 125
            elif 126 <= int(percent):
                bonuspercent = 150
            else:
                bonuspercent = 0
            return bonuspercent

        # no quantity here
        amountspent = y
        percent = percentage(percent=((amountspent)), whole=standardpricefactor_btc)
        adjusted = bonus(percent=percent)
        points = points_trade
        addpoints = int((currentPoints + points + adjusted + btcbonus))
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)

        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up
        exp = int(points + adjusted + btcbonus)
        exptot = exptable(
            userid=user,
            type=15,
            amount=exp,
            timestamp=now,
        )
        db.session.add(guser)
        db.session.add(exptot)

    #Digital Trade
    elif type == 20:
        def percentage(percent, whole):
            c = ((Decimal(percent) / Decimal(whole)) * 100)
            return int(Decimal(c))
        # adds more if they spent more
        def bonus(percent):
            if 0 == int(percent):
                bonuspercent = 1
            elif 1 <= int(percent) <= 10:
                bonuspercent = 1
            elif 10 <= int(percent) <= 25:
                bonuspercent = 5
            elif 26 <= int(percent) <= 50:
                bonuspercent = 10
            elif 51 <= int(percent) <= 75:
                bonuspercent = 25
            elif 76 <= int(percent) <= 100:
                bonuspercent = 50
            elif 100 <= int(percent) <= 125:
                bonuspercent = 75
            elif 126 <= int(percent):
                bonuspercent = 100
            else:
                bonuspercent = 0
            return bonuspercent

        amountspent = y*quantity
        percent = percentage(percent=((amountspent)), whole=standardpricefactor)
        adjusted = bonus(percent=percent)
        points = points_sale
        addpoints = int((currentPoints + points + adjusted + digbonus))
        levels_up, exp_to_next = divmod(addpoints, experienceperlevel)
        exp = int(points + adjusted + digbonus)
        guser.experiencepoints = exp_to_next
        guser.level = guser.level + levels_up
        exptot = exptable(
            userid=user,
            type=20,
            amount=exp,
            timestamp=now,
        )
        db.session.add(guser)
        db.session.add(exptot)

    else:
        pass

    # if user sucks bad ..possibbly ban?
    if guser.level <= 0:
        guser.level = 0
        guser.experiencepoints = 999
        db.session.add(guser)

    # achievements
    levelawards(userid=guser.userid)
