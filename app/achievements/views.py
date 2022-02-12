from flask import \
    render_template, \
    redirect, \
    url_for, \
    flash, \
    request
from flask_login import current_user
from app.achievements import achievements
from app import db
from datetime import datetime
from app.common.decorators import \
    website_offline, \
    login_required
from app.common.functions import floating_decimals
from app.classes.profile import exptable
# forms
from app.auth.forms import achselectForm
# models
from app.classes.auth import User
from app.classes.achievements import \
    UserAchievements, \
    whichAch, \
    UserAchievements_recent, Achievements
from app.classes.profile import \
    StatisticsUser, \
    StatisticsVendor
from app.classes.wallet_bch import \
    BchWallet

def row2dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    my_none = '1'
    nodate = 'date'
    noid = 'id'
    nouser_id = 'user_id'
    nolevel = 'level'
    noexp = 'experiencepoints'
    nousername = 'username'
    solutions = []
    for key, value in d.items():

        if my_none in value:
            if nousername not in key:
                if nodate not in key:
                    if nolevel not in key:
                        if noid not in key:
                            if nouser_id not in key:
                                if noexp not in key:
                                    solutions.append(key)
    x = solutions
    size = len(x)
    return x, size

@achievements.route('/profile-achievements-all/<username>', methods=['GET'])
@website_offline
@login_required
def profile_achs(username):
    if request.method == 'GET':
 
            user = db.session\
                .query(User)\
                .filter_by(username=username)\
                .first()
            title = user.username + "'s Achievements"
            usergetlevel = db.session\
                .query(UserAchievements)\
                .filter_by(username=user.username)\
                .first()
            userpictureid = str(usergetlevel.level)
            userwallet = db.session\
                .query(BchWallet)\
                .filter_by(user_id=user.id)\
                .first()
            userstats = db.session\
                .query(StatisticsUser)\
                .filter_by(username=user.username)\
                .first()
            level = db.session\
                .query(UserAchievements)\
                .first()
            nextlevel = level.level + 1
            userach = db.session\
                .query(whichAch)\
                .filter_by(user_id=user.id)\
                .first()
            user_recent_ach = db.session\
                .query(UserAchievements_recent)\
                .filter_by(user_id=user.id)\
                .order_by(UserAchievements_recent.achievement_date.desc())\
                .limit(10)

            if 1 <= level.level <= 3:
                user1widthh = (level.experiencepoints / 300) * 100
                width = floating_decimals(user1widthh, 0)
            elif 4 <= level.level <= 7:
                user1widthh = (level.experiencepoints / 500) * 100
                width = floating_decimals(user1widthh, 0)
            elif 8 <= level.level <= 10:
                user1widthh = (level.experiencepoints / 1000) * 100
                width = floating_decimals(user1widthh, 0)
            elif 11 <= level.level <= 14:
                user1widthh = (level.experiencepoints / 1500) * 100
                width = floating_decimals(user1widthh, 0)
            elif 16 <= level.level <= 20:
                user1widthh = (level.experiencepoints / 2000) * 100
                width = floating_decimals(user1widthh, 0)
            elif 21 <= level.level <= 25:
                user1widthh = (level.experiencepoints / 2250) * 100
                width = floating_decimals(user1widthh, 0)
            elif 26 <= level.level <= 30:
                user1widthh = (level.experiencepoints / 2500) * 100
                width = floating_decimals(user1widthh, 0)
            elif 26 <= level.level <= 30:
                user1widthh = (level.experiencepoints / 3000) * 100
                width = floating_decimals(user1widthh, 0)
            elif 26 <= level.level <= 30:
                user1widthh = (level.experiencepoints / 4000) * 100
                width = floating_decimals(user1widthh, 0)
            elif 30 <= level.level <= 50:
                user1widthh = (level.experiencepoints / 5000) * 100
                width = floating_decimals(user1widthh, 0)
            elif 51 <= level.level <= 100:
                user1widthh = (level.experiencepoints / 10000) * 100
                width = floating_decimals(user1widthh, 0)
            else:
                user1widthh = (level.experiencepoints / 1000) * 100
                width = floating_decimals(user1widthh, 0)

            # getuser exp table
            userexp = db.session\
                .query(exptable)\
                .filter(user.id == exptable.user_id)\
                .order_by(exptable.timestamp.desc())
            exp = userexp.limit(10)
            expcount = userexp.count()
            return render_template('/profile/userachievements/achievementsall.html',
                                title=title,
                                user=user,
                                width=width,
                                level=level,
                                usergetlevel=usergetlevel,
                                userpictureid=userpictureid,
                                userwallet=userwallet,
                                userstats=userstats,
                                exp=exp, expcount=expcount,
                                userach=userach,
                                nextlevel=nextlevel,
                                user_recent_ach=user_recent_ach
                                )

@achievements.route('/profile-achievements-coin/<username>', methods=['GET'])
@website_offline
def profile_achievements_coin(username):
    if request.method == 'GET':

        user = db.session.query(User).filter_by(username=username).first()
        title = user.username + "'s Achievements"

        x, size = row2dict(row=db.session.query(
            UserAchievements).filter_by(user_id=user.id).first())

        return render_template('/profile/userachievements/achievementscoin.html',
                            x=x,
                            size=size,
                            title=title,
                            user=user
                            )


@achievements.route('/profile-achievements-common/<username>', methods=['GET'])
@website_offline
def profile_achievements_common(username):
    if request.method == 'GET':
        user = db.session.query(User).filter_by(username=username).first()
        title = user.username + "'s Achievements"


        x, size = row2dict(row=db.session.query(UserAchievements).filter_by(user_id=user.id).first())
        return render_template('/profile/userachievements/achievementscommon.html',
                            x=x,
                            size=size,
                            title=title,
                            user=user
                            )


@achievements.route('/profile-achievements-experience/<username>', methods=['GET'])
@website_offline
def profile_achievements_experience(username):
    if request.method == 'GET':
        user = db.session.query(User).filter_by(username=username).first()
        title = user.username + "'s Achievements"

        x, size = row2dict(row=db.session.query(
            UserAchievements).filter_by(user_id=user.id).first())
        return render_template('/profile/userachievements/achievementsExperience.html',
                            x=x,
                            size=size,
                            title=title,
                            user=user
                            )


@achievements.route('/profile-auth-achievements-unique/<username>', methods=['GET'])
@website_offline
def profile_achievements_unique(username):
    if request.method == 'GET':
        user = db.session.query(User).filter_by(username=username).first()
        title = user.username + "'s Achievements"

        x, size = row2dict(row=db.session.query(
            UserAchievements).filter_by(user_id=user.id).first())
        return render_template('/profile/userachievements/achievementsunique.html',
                            x=x,
                            size=size,
                            title=title,
                            user=user
                            )


@achievements.route('/profile-achievements-customer/<username>', methods=['GET'])
@website_offline
def profile_achievements_customer(username):
    if request.method == 'GET':
        user = db.session.query(User).filter_by(username=username).first()
        title = user.username + "'s Achievements"



        x, size = row2dict(row=db.session.query(
            UserAchievements).filter_by(user_id=user.id).first())
        return render_template('/profile/userachievements/achievementscustomer.html',
                            x=x,
                            size=size,
                            title=title,
                            user=user
                            )


@achievements.route('/profile-achievements-vendor/<username>', methods=['GET'])
@website_offline
def profile_achievements_vendor(username):
    if request.method == 'GET':
        user = db.session.query(User).filter_by(username=username).first()
        title = user.username + "'s Achievements"
        x, size = row2dict(row=db.session.query(
            UserAchievements).filter_by(user_id=user.id).first())
        return render_template('/profile/userachievements/achievementsvendor.html',
                            x=x,
                            size=size,
                            title=title,
                            user=user
                           )


@achievements.route('/profile-allachievements', methods=['GET'])
def profile_allachievements_main_home():
    if request.method == 'GET':
        title = "All Achievements"
        achievements = db.session\
            .query(Achievements)\
            .order_by(Achievements.dateadded.desc())\
            .all()
        return render_template('/achievements/achievementsall.html',
                            title=title,
                            achievements=achievements,
                            )


@achievements.route('/profile-achievementscommon', methods=['GET'])
def profile_achievements_common_home():
    if request.method == 'GET':    
        title = "Common Achievements"
        achievements = db.session\
            .query(Achievements)\
            .filter_by(category=1)\
            .all()
        return render_template('/achievements/achievementscommon.html',
                            title=title,
                            achievements=achievements,
                            )


@achievements.route('/profile-achievementsExperience', methods=['GET'])
def profile_achievements_experience_home():
    if request.method == 'GET':    
        title = "Experience Achievements"
        achievements = db.session\
            .query(Achievements)\
            .filter_by(category=2)\
            .all()
        return render_template('/achievements/achievementsExperience.html',
                            title=title,
                            achievements=achievements,
                            )


@achievements.route('/all-achievementsCustmer', methods=['GET'])
def achievements_customer_home():
    if request.method == 'GET':
        title = "Customer Achievements"
        achievements = db.session\
            .query(Achievements)\
            .filter_by(category=3)\
            .all()
        return render_template('/achievements/achievementscustomer.html',
                            title=title,
                            achievements=achievements,
                            )


@achievements.route('/all-achievementsVendor', methods=['GET'])
def achievements_vendor_home():
    if request.method == 'GET':
    
        title = "Vendor Achievements"
        achievements = db.session\
            .query(Achievements)\
            .filter_by(category=4)\
            .all()
        return render_template('/achievements/achievementsvendor.html',
                            title=title,
                            achievements=achievements,
                            )


@achievements.route('/all-achievements/coin', methods=['GET'])
def achievements_coin_home():
    if request.method == 'GET':
    
        title = "Coin Achievements"
        achievements = db.session\
            .query(Achievements)\
            .filter_by(category=5)\
            .all()
        return render_template('/achievements/achievementscoin.html',
                            title=title,
                            achievements=achievements,
                            )


@achievements.route('/all-achievements/unique', methods=['GET'])
def achievements_unique_home():
    if request.method == 'GET':
    
        title = "Unique Achievements"
        achievements = db.session\
            .query(Achievements)\
            .filter_by(category=6)\
            .all()
        return render_template('/achievements/achievementsunique.html',
                            title=title,
                            achievements=achievements,
                            )


@achievements.route('/allachievements/all', methods=['GET'])
@website_offline
def achievements_all_home():
    if request.method == 'GET':
        title = current_user.username + "'s Achievements"
        x, size = row2dict(row=db.session
                        .query(UserAchievements)
                        .filter_by(user_id=current_user.id)
                        .first())
        return render_template('/auth/userachievements/achievementsall.html',
                            x=x,
                            size=size,
                            title=title
                            )


@achievements.route('/auth-achievements-coin/', methods=['GET'])
@website_offline
def auth_achievements_coin():
    if request.method == 'GET':
        title = current_user.username + "'s Achievements"
        x, size = row2dict(row=db.session
                        .query(UserAchievements)
                        .filter_by(user_id=current_user.id)
                        .first())

        return render_template('/auth/userachievements/achievementscoin.html',
                            x=x,
                            size=size,
                            title=title
                            )


@achievements.route('/auth-achievements-common/', methods=['GET'])
@website_offline
def auth_achievements_common():
    if request.method == 'GET':

        title = current_user.username + "'s Achievements"

        x, size = row2dict(row=db.session
                        .query(UserAchievements)
                        .filter_by(user_id=current_user.id)
                        .first())
        return render_template('/auth/userachievements/achievementscommon.html',
                            x=x,
                            size=size,
                            title=title
                            )


@achievements.route('/auth-achievements-experience/', methods=['GET'])
@website_offline
def auth_achievements_experience():
    if request.method == 'GET':
        
        title = current_user.username + "'s Achievements"

        x, size = row2dict(row=db.session
                        .query(UserAchievements)
                        .filter_by(user_id=current_user.id)
                        .first())
        return render_template('/auth/userachievements/achievementsExperience.html',
                            x=x,
                            size=size,
                            title=title
                            )


@achievements.route('/auth-achievements-unique/', methods=['GET'])
@website_offline
def auth_achievements_unique():
    if request.method == 'GET':

        title = current_user.username + "'s Achievements"
        x, size = row2dict(row=db.session
                        .query(UserAchievements)
                        .filter_by(user_id=current_user.id)
                        .first())
        return render_template('/auth/userachievements/achievementsunique.html',
                            x=x,
                            size=size,
                            title=title
                            )


@achievements.route('/auth-achievements-customer/', methods=['GET'])
@website_offline
def auth_achievements_customer():
    if request.method == 'GET':
    
        title = current_user.username + "'s Achievements"

        x, size = row2dict(row=db.session
                        .query(UserAchievements)
                        .filter_by(user_id=current_user.id)
                        .first())
        return render_template('/auth/userachievements/achievementscustomer.html',
                            x=x,
                            size=size,
                            title=title
                            )


@achievements.route('/auth-achievements-vendor/', methods=['GET'])
@website_offline
def auth_achievements_vendor():
    if request.method == 'GET':

        title = current_user.username + "'s Achievements"

        x, size = row2dict(row=db.session
                        .query(UserAchievements)
                        .filter_by(user_id=current_user.id)
                        .first())
        return render_template('/auth/userachievements/achievementsvendor.html',
                            x=x,
                            size=size,
                            title=title
                            )


@achievements.route('/select-user-achievements/', methods=['GET', 'POST'])
@website_offline
def selectuserachs():
    if request.method == 'GET':

        title = "My Achievements"
        form = achselectForm()
        now = datetime.utcnow()
        specificach = db.session.query(whichAch).filter_by(
            user_id=current_user.id).first()
        if current_user.vendor_account == 0:
            user = db.session.query(User).filter_by(
                username=current_user.username).first()
            usergetlevel = db.session.query(UserAchievements).filter_by(
                username=user.username).first()
            userpictureid = str(usergetlevel.level)
            userwallet = db.session.query(
                BchWallet).filter_by(user_id=user.id).first()
            userstats = db.session.query(StatisticsUser).filter_by(
                username=user.username).first()

            level = db.session.query(UserAchievements).filter_by(
                username=user.username).first()
            width = int(level.experiencepoints / 10)
            userach = db.session.query(whichAch).filter_by(
                user_id=current_user.id).first()
            vendor = 0
            vendorwallet = 0
            vendorstats = 0
            vendorgetlevel = 0
            vendorpictureid = 0
            vendorach = 0
        else:
            # vendor
            vendor = db.session\
                .query(User)\
                .filter_by(id=current_user.id)\
                .first()
            vendorwallet = db.session\
                .query(BchWallet)\
                .filter_by(user_id=vendor.id)\
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
            vendorach = db.session\
                .query(whichAch)\
                .filter_by(user_id=current_user.id)\
                .first()

            user = 0
            usergetlevel = 0
            userpictureid = 0
            userwallet = 0
            userstats = 0
            userach = 0

            level = 0
            width = 0

        x, size = row2dict(row=db.session.query(UserAchievements).filter_by(user_id=current_user.id).first())
        return render_template('/auth/userachievements/achievementscustomize.html',
                            x=x,
                            size=size,
                            title=title,
                            form=form,
                            specificach=specificach,
                            user=user,
                            now=now,
                            usergetlevel=usergetlevel,
                            userpictureid=userpictureid,
                            userwallet=userwallet,
                            userstats=userstats,
                            width=width,
                            level=level,
                            vendor=vendor,
                            vendorwallet=vendorwallet,
                            vendorstats=vendorstats,
                            vendorgetlevel=vendorgetlevel,
                            vendorpictureid=vendorpictureid,
                            userach=userach,
                            vendorach=vendorach
                            )

    if request.method == "POST":
        if form.selectone.data:
            if form.ach1.data == specificach.ach2 \
                    or form.ach1.data == specificach.ach3 \
                    or form.ach1.data == specificach.ach4 \
                    or form.ach1.data == specificach.ach5:
                flash("you already have that achievement listed", category='danger')
                return redirect(url_for('achievements.selectuserachs'))
            else:

                full = form.ach1.data
                if full in x:
                    cat = full[0]
                    specificach.ach1 = form.ach1.data,
                    specificach.ach1_cat = cat,

                    db.session.add(specificach)
                    db.session.commit()
                else:
                    flash("You dont have that achievement", category='danger')
                    return redirect(url_for('achievements.selectuserachs'))

        elif form.selecttwo.data:
            if form.ach2.data == specificach.ach1 \
                    or form.ach2.data == specificach.ach3 \
                    or form.ach2.data == specificach.ach4 \
                    or form.ach2.data == specificach.ach5:
                flash("you already have that achievement listed", category='danger')
                return redirect(url_for('achievements.selectuserachs'))
            else:
                full = form.ach2.data
                if full in x:
                    cat = full[0]
                    specificach.ach2 = form.ach2.data,
                    specificach.ach2_cat = cat,
                    db.session.add(specificach)
                    db.session.commit()
                else:
                    flash("You dont have that achievement", category='danger')
                    return redirect(url_for('achievements.selectuserachs'))
        elif form.selectthree.data:
            if form.ach3.data == specificach.ach2 \
                    or form.ach3.data == specificach.ach1 \
                    or form.ach3.data == specificach.ach4 \
                    or form.ach3.data == specificach.ach5:
                flash("you already have that achievement listed", category='danger')
                return redirect(url_for('achievements.selectuserachs'))
            else:
                full = form.ach3.data
                if full in x:
                    cat = full[0]
                    specificach.ach3 = form.ach3.data,
                    specificach.ach3_cat = cat,
                    db.session.add(specificach)
                    db.session.commit()
                else:
                    flash("You dont have that achievement", category='danger')
                    return redirect(url_for('achievements.selectuserachs'))

        elif form.selectfour.data:
            if form.ach4.data == specificach.ach2 \
                    or form.ach4.data == specificach.ach3 \
                    or form.ach4.data == specificach.ach1 \
                    or form.ach4.data == specificach.ach5:
                flash("you already have that achievement listed", category='danger')
                return redirect(url_for('achievements.selectuserachs'))
            else:
                full = form.ach4.data
                if full in x:
                    cat = full[0]
                    specificach.ach4 = form.ach4.data,
                    specificach.ach4_cat = cat,
                    db.session.add(specificach)
                    db.session.commit()
                else:
                    flash("You dont have that achievement", category='danger')
                    return redirect(url_for('achievements.selectuserachs'))
        elif form.selectfive.data:
            if form.ach5.data == specificach.ach2 \
                    or form.ach5.data == specificach.ach3 \
                    or form.ach5.data == specificach.ach4 \
                    or form.ach5.data == specificach.ach1:
                flash("you already have that achievement listed", category='danger')
                return redirect(url_for('achievements.selectuserachs'))
            else:
                full = form.ach5.data
                if full in x:
                    cat = full[0]
                    specificach.ach5 = form.ach5.data,
                    specificach.ach5_cat = cat,

                    db.session.add(specificach)
                    db.session.commit()
                else:
                    flash("You dont have that achievement", category='danger')
                    return redirect(url_for('achievements.selectuserachs'))

        elif form.deleteone.data:
            specificach.ach1 = '0',
            specificach.ach1_cat = '0',
            db.session.add(specificach)
            db.session.commit()

        elif form.deletetwo.data:
            specificach.ach2 = '0',
            specificach.ach2_cat = '0',
            db.session.add(specificach)
            db.session.commit()

        elif form.deletethree.data:
            specificach.ach3 = '0',
            specificach.ach3_cat = '0',
            db.session.add(specificach)
            db.session.commit()

        elif form.deletefour.data:
            specificach.ach4 = '0',
            specificach.ach4_cat = '0',
            db.session.add(specificach)
            db.session.commit()

        elif form.deletefive.data:
            specificach.ach5 = '0',
            specificach.ach5_cat = '0',
            db.session.add(specificach)
            db.session.commit()
        else:
            pass

        return render_template('/auth/userachievements/achievementscustomize.html',
                            x=x,
                            size=size,
                            title=title,
                            form=form,
                            specificach=specificach,
                            user=user,
                            now=now,
                            usergetlevel=usergetlevel,
                            userpictureid=userpictureid,
                            userwallet=userwallet,
                            userstats=userstats,
                            width=width,
                            level=level,
                            vendor=vendor,
                            vendorwallet=vendorwallet,
                            vendorstats=vendorstats,
                            vendorgetlevel=vendorgetlevel,
                            vendorpictureid=vendorpictureid,
                            userach=userach,
                            vendorach=vendorach
                            )
