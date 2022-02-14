from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.message import message
from app import db

from datetime import datetime

from app.message.forms import\
    addusertoconvoForm,\
    CommentForm,\
    sendmessageForm, \
    allActionForm,\
    topbuttonForm

# models
from app.classes.auth import Auth_User

from app.classes.message import \
    Message_Post, \
    Message_PostUser, \
    Message_Comment

from app.notification import notification
from flask_paginate import Pagination, get_page_args

from app.common.decorators import login_required, ping_user


@message.route('/message_center', methods=['GET', 'POST'])
@login_required
def message_center():
    
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    delormarkasread = topbuttonForm()
    title = 'Messages'
    
    # sidebar stuff
    # Get New messages count
    newmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.unread == 1)
    allmsgcount = newmsg.count()
    
    # get read msg count
    oldmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.unread == 0)
    oldmsgcount = oldmsg.count()

    # Get official Count
    officialmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.official == 1, Message_PostUser.dispute == 0, Message_PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # Get Disputes Count
    disputesmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.dispute == 1, Message_PostUser.unread == 1)
    disputesmsgcount = disputesmsg.count()

    # Get all msgs for current page
    allmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.unread == 1)\
        .order_by(Message_PostUser.timestamp.desc())

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

    # pagination quewry
    posts = allmsg.limit(per_page).offset(offset)
    postcount = allmsg.count()

    pagination = Pagination(page=page,
                            total=allmsg.count(),
                            search=search,
                            record_name='ratings',
                            offset=offset,
                            per_page=per_page,
                            css_framework='bootstrap4',
                            inner_window=inner_window,
                            outer_window=outer_window)

    if request.method == "POST":
        for v in request.form.getlist('checkit'):
            specific_post = db.session.query(
                Message_PostUser).filter_by(id=v).first()
            if delormarkasread.delete.data:
                if specific_post.user_id == current_user.id:
                    db.session.delete(specific_post)
            elif delormarkasread.markasread.data:
                if specific_post.user_id == current_user.id:
                    specific_post.unread = 0
                    db.session.add(specific_post)
            else:
                pass
        db.session.commit()
        return redirect(url_for('message.message_center', username=current_user.username))

    return render_template('messages/main.html',
                           now=now,
                           title=title,
                           posts=posts,
                           aform=aform,
                           pagination=pagination,
                           allmsgcount=allmsgcount,
                           officialmsgcount=officialmsgcount,
                           disputesmsgcount=disputesmsgcount,
                           oldmsgcount=oldmsgcount,
                           delormarkasread=delormarkasread,
                           postcount=postcount
                           )


@message.route('/message_center-disputes', methods=['GET', 'POST'])
@login_required
def message_disputes():
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    delormarkasread = topbuttonForm()
    user = db.session\
        .query(Auth_User)\
        .filter_by(username=current_user.username)\
        .first()
    title = 'Disputes'

    # sidebar stuff
    # Get New messages count
    newmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.unread == 1)

    allmsgcount = newmsg.count()

    # Get official Count
    officialmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.official == 1, Message_PostUser.dispute == 0, Message_PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # get read msg count
    # get read msg count
    oldmsg = db.session.query(Message_PostUser)
    oldmsg = oldmsg.filter(Message_PostUser.user_id == current_user.id)
    oldmsg = oldmsg.filter(Message_PostUser.unread == 0)

    oldmsgcount = oldmsg.count()
    # Get Disputes Count
    disputesmsg = db.session.query(Message_PostUser)
    disputesmsg = disputesmsg.filter(
        Message_PostUser.user_id == current_user.id)
    disputesmsg = disputesmsg.filter(Message_PostUser.dispute == 1)
    disputesmsgcount = disputesmsg.count()

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

    posts = disputesmsg.limit(per_page).offset(offset)
    postcount = disputesmsg.count()
    pagination = Pagination(page=page,
                            total=disputesmsg.count(),
                            search=search,
                            record_name='ratings',
                            offset=offset,
                            per_page=per_page,
                            css_framework='bootstrap4',
                            inner_window=inner_window,
                            outer_window=outer_window,
                            )

    if request.method == "POST":
        try:
            for v in request.form.getlist('checkit'):
                specific_post = db.session.query(
                    Message_PostUser).filter_by(id=v).first()
                if delormarkasread.delete.data:
                    if specific_post.user_id == current_user.id:
                        db.session.delete(specific_post)

                elif delormarkasread.markasread.data:
                    if specific_post.user_id == current_user.id:
                        specific_post.unread = 0
                        db.session.add(specific_post)

                else:
                    pass
            db.session.commit()
            return redirect(url_for('message.message_center', username=current_user.username))
        except:
            return redirect(url_for('index', username=current_user.username))

    return render_template('messages/disputes.html',
                           user=user, now=now,
                           title=title,
                           posts=posts,
                           aform=aform,
                           oldmsgcount=oldmsgcount,
                           officialmsgcount=officialmsgcount,
                           disputesmsgcount=disputesmsgcount,
                           allmsgcount=allmsgcount,
                           pagination=pagination,
                           delormarkasread=delormarkasread,
                           postcount=postcount
                           )


@message.route('/messagecenterold', methods=['GET', 'POST'])
@login_required
def message_old_msgs():
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    delormarkasread = topbuttonForm()
    user = Auth_User.query.filter_by(username=current_user.username).first()
    title = 'Old Messages'

    # sidebar stuff
    # Get New messages count
    newmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.unread == 1)

    allmsgcount = newmsg.count()

    # Get official Count
    officialmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.official == 1, Message_PostUser.dispute == 0, Message_PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # Get Disputes Count
    disputesmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.dispute == 1)
    disputesmsgcount = disputesmsg.count()

    # get read msg count
    oldmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.unread == 0)\
        .order_by(Message_PostUser.timestamp.desc())

    oldmsgcount = oldmsg.count()
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page, per_page, offset = get_page_args()

    # PEr Page tells how many search results pages

    inner_window = 5  # search bar at bottom used for .. lots of pages
    outer_window = 5  # search bar at bottom used for .. lots of pages
    per_page = 10

    posts = oldmsg.limit(per_page).offset(offset)

    postcount = disputesmsg.count()
    pagination = Pagination(page=page,
                            total=oldmsg.count(),
                            search=search,
                            record_name='ratings',
                            offset=offset,
                            per_page=per_page,
                            css_framework='bootstrap4',
                            inner_window=inner_window,
                            outer_window=outer_window,
                            )

    if request.method == "POST":
        try:
            for v in request.form.getlist('checkit'):
                specific_post = db.session.query(
                    Message_PostUser).filter_by(id=v).first()
                if delormarkasread.delete.data:
                    if specific_post.user_id == current_user.id:
                        db.session.delete(specific_post)

                elif delormarkasread.markasread.data:
                    if specific_post.user_id == current_user.id:
                        specific_post.unread = 0
                        db.session.add(specific_post)
                else:
                    pass
            db.session.commit()
            return redirect(url_for('message.message_center', username=current_user.username))
        except:
            return redirect(url_for('index', username=current_user.username))

    return render_template('messages/oldmessages.html',
                           user=user, now=now,
                           title=title,
                           posts=posts,
                           aform=aform,
                           oldmsgcount=oldmsgcount,
                           officialmsgcount=officialmsgcount,
                           disputesmsgcount=disputesmsgcount,
                           allmsgcount=allmsgcount,
                           pagination=pagination,
                           delormarkasread=delormarkasread,
                           postcount=postcount
                           )


@message.route('/message_center-official', methods=['GET', 'POST'])
@login_required
def message_official():
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    delormarkasread = topbuttonForm()
    user = db.session\
        .query(Auth_User)\
        .filter_by(username=current_user.username)\
        .first()
    title = 'Official Messages'

    # sidebar stuff
    # Get New messages count
    newmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.unread == 1)
    allmsgcount = newmsg.count()

    # get read msg count
    oldmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.unread == 0)
    oldmsgcount = oldmsg.count()

    # Get official Count
    officialmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.official == 1, Message_PostUser.dispute == 0, Message_PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # Get Disputes Count
    disputesmsg = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.dispute == 1, Message_PostUser.unread == 1)
    disputesmsgcount = disputesmsg.count()

    # Get official Count
    officialmsginbox = db.session\
        .query(Message_PostUser)\
        .filter(Message_PostUser.user_id == current_user.id)\
        .filter(Message_PostUser.official == 1, Message_PostUser.dispute == 0)

    # pagination
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page, per_page, offset = get_page_args()

    # PEr Page tells how many search results pages

    inner_window = 5  # search bar at bottom used for .. lots of pages
    outer_window = 5  # search bar at bottom used for .. lots of pages
    per_page = 10

    posts = officialmsginbox.limit(per_page).offset(offset)
    postcount = officialmsginbox.count()
    pagination = Pagination(page=page,
                            total=officialmsg.count(),
                            search=search,
                            record_name='ratings',
                            offset=offset,
                            per_page=per_page,
                            css_framework='bootstrap4',
                            inner_window=inner_window,
                            outer_window=outer_window)

    if request.method == "POST":
        try:
            for v in request.form.getlist('checkit'):
                specific_post = db.session.query(
                    Message_PostUser).filter_by(id=v).first()
                if delormarkasread.delete.data:
                    if specific_post.user_id == current_user.id:
                        db.session.delete(specific_post)

                elif delormarkasread.markasread.data:
                    if specific_post.user_id == current_user.id:
                        specific_post.unread = 0
                        db.session.add(specific_post)

                else:
                    pass
            db.session.commit()
            return redirect(url_for('message.message_center', username=current_user.username))
        except:
            return redirect(url_for('index', username=current_user.username))

    return render_template('messages/official.html',
                           user=user, now=now,
                           title=title,
                           posts=posts,
                           aform=aform,
                           oldmsgcount=oldmsgcount,
                           officialmsgcount=officialmsgcount,
                           disputesmsgcount=disputesmsgcount,
                           allmsgcount=allmsgcount,
                           pagination=pagination,
                           delormarkasread=delormarkasread,
                           postcount=postcount
                           )


@message.route('/message_center-sent', methods=['GET', 'POST'])
@login_required
def message_sent():
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    delormarkasread = topbuttonForm()
    user = db.session\
        .query(Auth_User)\
        .filter_by(username=current_user.username)\
        .first()
    title = 'Sent'

    # sidebar stuff
    # Get New messages count
    newmsg = db.session.query(Message_PostUser)
    newmsg = newmsg.filter(Message_PostUser.user_id == current_user.id)
    newmsg = newmsg.filter(Message_PostUser.unread == 1)

    allmsgcount = newmsg.count()

    # Get official Count
    officialmsg = db.session.query(Message_PostUser)
    officialmsg = officialmsg.filter(
        Message_PostUser.user_id == current_user.id)
    officialmsg = officialmsg.filter(
        Message_PostUser.official == 1, Message_PostUser.dispute == 0, Message_PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # Get Disputes Count
    disputesmsg = db.session.query(Message_PostUser)
    disputesmsg = disputesmsg.filter(
        Message_PostUser.dispute == 1, Message_PostUser.unread == 1)
    disputesmsgcount = disputesmsg.count()
    # get read msg count
    # get read msg count
    oldmsg = db.session.query(Message_PostUser)
    oldmsg = oldmsg.filter(Message_PostUser.user_id == current_user.id)
    oldmsg = oldmsg.filter(Message_PostUser.unread == 0)
    oldmsgcount = oldmsg.count()

    # Get sent msgs
    sentmsg = db.session.query(Message_PostUser)
    sentmsg = sentmsg.filter(Message_PostUser.author_id == current_user.id)
    sentmsg = sentmsg.filter(Message_PostUser.user_id == current_user.id)
    sentmsg = sentmsg.order_by(Message_PostUser.timestamp.desc())

    sentmsgcount = sentmsg.count()

    # pagination
    search = False
    q = request.args.get('q')
    if q:
        search = True

    page, per_page, offset = get_page_args()

    # PEr Page tells how many search results pages

    inner_window = 5  # search bar at bottom used for .. lots of pages
    outer_window = 5  # search bar at bottom used for .. lots of pages
    per_page = 10

    posts = sentmsg.limit(per_page).offset(offset)
    postcount = sentmsg.count()
    pagination = Pagination(page=page,
                            total=sentmsg.count(),
                            search=search,
                            record_name='ratings',
                            offset=offset,
                            per_page=per_page,
                            css_framework='bootstrap4',
                            inner_window=inner_window,
                            outer_window=outer_window)

    if request.method == "POST":
        try:
            for v in request.form.getlist('checkit'):
                specific_post = db.session.query(
                    Message_PostUser).filter_by(id=v).first()
                if delormarkasread.delete.data:
                    if specific_post.user_id == current_user.id:
                        db.session.delete(specific_post)

                elif delormarkasread.markasread.data:
                    if specific_post.user_id == current_user.id:
                        specific_post.unread = 0
                        db.session.add(specific_post)

                else:
                    pass
            db.session.commit()
            return redirect(url_for('message.message_center', username=current_user.username))
        except:
            return redirect(url_for('index', username=current_user.username))

    return render_template('messages/sent.html',
                           user=user, now=now,
                           title=title,
                           posts=posts,
                           aform=aform,
                           oldmsgcount=oldmsgcount,
                           officialmsgcount=officialmsgcount,
                           pagination=pagination,
                           disputesmsgcount=disputesmsgcount,
                           sentmsgcount=sentmsgcount,
                           delormarkasread=delormarkasread,
                           postcount=postcount,
                           allmsgcount=allmsgcount
                           )


@message.route('/message_center-compose', methods=['GET', 'POST'])
@login_required
def message_compose():
    now = datetime.utcnow()
    form = sendmessageForm(request.form)
    aform = allActionForm(request.form)

    user = Auth_User.query.filter_by(username=current_user.username).first()
    if user:
        pass
    else:
        flash("There is no user with the username " +
              form.username.data, category="danger")
        return redirect(url_for('message.message_compose', username=current_user.username))
    title = 'Compose Message'

    # sidebar stuff
    # Get New messages count
    newmsg = db.session.query(Message_PostUser)
    newmsg = newmsg.filter(Message_PostUser.user_id == current_user.id)
    newmsg = newmsg.filter(Message_PostUser.unread == 1)
    allmsgcount = newmsg.count()

    # Get official Count
    officialmsg = db.session.query(Message_PostUser)
    officialmsg = officialmsg.filter(
        Message_PostUser.user_id == current_user.id)
    officialmsg = officialmsg.filter(
        Message_PostUser.official == 1, Message_PostUser.dispute == 0, Message_PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # Get Disputes Count
    disputesmsg = db.session.query(Message_PostUser)
    disputesmsg = disputesmsg.filter(
        Message_PostUser.user_id == current_user.id)
    disputesmsg = disputesmsg.filter(
        Message_PostUser.dispute == 1, Message_PostUser.unread == 1)
    disputesmsgcount = disputesmsg.count()
    # get read msg count
    oldmsg = db.session.query(Message_PostUser)
    oldmsg = oldmsg.filter(Message_PostUser.user_id == current_user.id)
    oldmsg = oldmsg.filter(Message_PostUser.unread == 1)

    oldmsgcount = oldmsg.count()

    if request.method == 'POST' and form.validate_on_submit():

        usersearch = db.session.query(Auth_User).filter_by(
            username=form.username.data).first()
        if usersearch is None:
            flash("There is no user with the username " +
                  form.username.data, category="success")
            return redirect(url_for('message.message_compose', username=current_user.username))
        elif usersearch.username == current_user.username:
            flash("You cant send mail to yourself.", category="success")
            return redirect(url_for('message.message_compose', username=current_user.username))
        else:

            newpost = Message_Post(timestamp=now)
            db.session.add(newpost)

            db.session.flush()

            # create for person getting it
            userpost = Message_PostUser(
                # type of message
                official=0,
                dispute=0,
                usermsg=1,
                # info in msg
                body=form.body1.data,
                subject=form.subject.data,
                timestamp=now,
                author_id=current_user.id,
                itemid=0,
                unread=1,
                modid=0,
                postid=newpost.id,
                user_id=usersearch.id,
                username=usersearch.username

            )
            db.session.add(userpost)

            # create for author
            userpost2 = Message_PostUser(
                # type of message
                official=0,
                dispute=0,
                usermsg=1,
                # info in msg
                body=form.body1.data,
                subject=form.subject.data,
                timestamp=now,
                author_id=current_user.id,
                itemid=0,
                unread=0,
                modid=0,
                postid=newpost.id,
                user_id=current_user.id,
                username=current_user.username
            )
            db.session.add(userpost2)
            db.session.commit()
            flash("Message sent to " + form.username.data, category="success")
            notification(type=2, username=current_user.username,
                         user_id=current_user.id, salenumber=0, bitcoin=0)

            return redirect(url_for('message.message_center', username=current_user.username))

    return render_template('messages/compose.html',
                           user=user, now=now,
                           title=title,
                           form=form,
                           aform=aform,
                           oldmsgcount=oldmsgcount,
                           officialmsgcount=officialmsgcount,
                           disputesmsgcount=disputesmsgcount,
                           allmsgcount=allmsgcount,
                           )


@message.route('/message_center-compose-specific/<person>/', methods=['GET', 'POST'])
@login_required
def message_compose_specific_person(person):
    now = datetime.utcnow()
    if current_user.admin > 0:
        return redirect(url_for('message.message_compose_specific_person_admin', person=person))
    else:
        form = sendmessageForm(request.form)
        aform = allActionForm(request.form)
        user = db.session.query(Auth_User).filter_by(username=person).first()
        if user:
            # sidebar stuff
            # Get New messages count
            newmsg = db.session.query(Message_PostUser)
            newmsg = newmsg.filter(Message_PostUser.user_id == current_user.id)
            newmsg = newmsg.filter(Message_PostUser.unread == 1)

            allmsgcount = newmsg.count()

            # Get official Count
            officialmsg = db.session.query(Message_PostUser)
            officialmsg = officialmsg.filter(
                Message_PostUser.user_id == current_user.id)
            officialmsg = officialmsg.filter(
                Message_PostUser.official == 1, Message_PostUser.dispute == 0, Message_PostUser.unread == 1)
            officialmsgcount = officialmsg.count()

            # Get Disputes Count
            disputesmsg = db.session.query(Message_PostUser)
            disputesmsg = disputesmsg.filter(
                Message_PostUser.user_id == current_user.id)
            disputesmsg = disputesmsg.filter(
                Message_PostUser.dispute == 1, Message_PostUser.unread == 1)
            disputesmsgcount = disputesmsg.count()

            # get read msg count
            oldmsg = db.session.query(Message_PostUser)
            oldmsg = oldmsg.filter(Message_PostUser.user_id == current_user.id)
            oldmsg = oldmsg.filter(Message_PostUser.unread == 1)

            oldmsgcount = oldmsg.count()

            if request.method == 'POST':
                if form.validate_on_submit():

                    post = Message_Post(
                        timestamp=now
                    )
                    db.session.add(post)
                    db.session.flush()

                    # create postuser for author
                    userpost2 = Message_PostUser(
                        # type of message
                        official=0,
                        dispute=0,
                        usermsg=1,
                        # info in msg
                        body=form.body1.data,
                        subject=form.subject.data,
                        timestamp=now,
                        author_id=current_user.id,
                        itemid=0,
                        unread=0,
                        modid=0,
                        postid=post.id,
                        user_id=current_user.id,
                        username=current_user.username
                    )
                    db.session.add(userpost2)

                    # create postuser for person getting it
                    userpost = Message_PostUser(
                        # type of message
                        official=0,
                        dispute=0,
                        usermsg=1,
                        # info in msg
                        body=form.body1.data,
                        subject=form.subject.data,
                        timestamp=now,
                        author_id=current_user.id,
                        modid=0,
                        itemid=0,
                        unread=1,
                        postid=post.id,
                        user_id=user.id,
                        username=user.username
                    )
                    db.session.add(userpost)
                    db.session.commit()
                    notification(type=2, username=user.username,
                                 user_id=user.id, salenumber=0, bitcoin=0)
                    flash("Message sent to " + user.username, category="success")
                    return redirect(url_for('message.message_center', username=current_user.username))

                else:
                    flash("Form Error", category="danger")
            return render_template('messages/composespecificperson.html',
                                   user=user, now=now,
                                   form=form,
                                   aform=aform,
                                   oldmsgcount=oldmsgcount,
                                   allmsgcount=allmsgcount,
                                   officialmsgcount=officialmsgcount,
                                   disputesmsgcount=disputesmsgcount,
                                   )
        else:
            flash("User doesnt exist: " + user.username, category="danger")
            return redirect(url_for('message.message_center', username=current_user.username))


@message.route('/message_center-compose-specific-admin/<person>/', methods=['GET', 'POST'])
@login_required
def message_compose_specific_person_admin(person):
    now = datetime.utcnow()

    if current_user.admin == 0:
        return redirect(url_for('index'))
    else:
        form = sendmessageForm(request.form)
        aform = allActionForm(request.form)
        user = db.session.query(Auth_User).filter_by(username=person).first()
        if user:
            # sidebar stuff
            # Get New messages count
            newmsg = db.session.query(Message_PostUser)
            newmsg = newmsg.filter(Message_PostUser.user_id == current_user.id)
            newmsg = newmsg.filter(Message_PostUser.unread == 1)

            allmsgcount = newmsg.count()

            # Get official Count
            officialmsg = db.session.query(Message_PostUser)
            officialmsg = officialmsg.filter(
                Message_PostUser.user_id == current_user.id)
            officialmsg = officialmsg.filter(
                Message_PostUser.official == 1, Message_PostUser.dispute == 0, Message_PostUser.unread == 1)
            officialmsgcount = officialmsg.count()

            # Get Disputes Count
            disputesmsg = db.session.query(Message_PostUser)
            disputesmsg = disputesmsg.filter(
                Message_PostUser.user_id == current_user.id)
            disputesmsg = disputesmsg.filter(
                Message_PostUser.dispute == 1, Message_PostUser.unread == 1)
            disputesmsgcount = disputesmsg.count()

            # get read msg count
            oldmsg = db.session.query(Message_PostUser)
            oldmsg = oldmsg.filter(Message_PostUser.user_id == current_user.id)
            oldmsg = oldmsg.filter(Message_PostUser.unread == 0)

            oldmsgcount = oldmsg.count()
            if request.method == 'POST':

                try:
                    newpost = Message_Post(
                        timestamp=now
                    )
                    db.session.add(newpost)
                    db.session.flush()

                    # create postuser for author
                    userpost2 = Message_PostUser(
                        # type of message
                        official=1,
                        dispute=0,
                        usermsg=1,
                        # info in msg
                        body=form.body1.data,
                        subject=form.subject.data,
                        timestamp=now,
                        author_id=current_user.id,
                        itemid=0,
                        unread=0,
                        modid=0,
                        postid=newpost.id,
                        user_id=current_user.id,
                        username=current_user.username

                    )
                    db.session.add(userpost2)

                    # create postuser for person getting it
                    userpost = Message_PostUser(
                        # type of message
                        official=1,
                        dispute=0,
                        usermsg=1,
                        # info in msg
                        body=form.body1.data,
                        subject=form.subject.data,
                        timestamp=now,
                        author_id=current_user.id,
                        modid=0,
                        itemid=0,
                        unread=1,
                        postid=post.id,
                        user_id=user.id,
                        username=user.username

                    )
                    db.session.add(userpost)
                    db.session.commit()
                    notification(type=2,
                                 username=user.username,
                                 user_id=user.id,
                                 salenumber=0,
                                 bitcoin=0
                                 )
                    flash("Message sent to " + user.username, category="success")
                    return redirect(url_for('message.message_center'))
                except:
                    db.session.rollback()
                    flash("Form Error", category="danger")
                    return redirect(url_for('message.message_compose_specific_person', person=current_user.username))
            return render_template('messages/adminmsgcompose.html',
                                   user=user, now=now,
                                   form=form,
                                   aform=aform,
                                   allmsgcount=allmsgcount,
                                   oldmsgcount=oldmsgcount,
                                   officialmsgcount=officialmsgcount,
                                   disputesmsgcount=disputesmsgcount,

                                   )
        else:
            flash("User doesnt exist: " + user.username, category="danger")
            return redirect(url_for('message.message_center', username=current_user.username))


@message.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def message_post(id):
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    form1 = CommentForm(request.form)
    form2 = addusertoconvoForm(request.form)
    post = db.session\
        .query(Message_Post)\
        .filter_by(id=id)\
        .first()
    if post:
        getpost = db.session\
            .query(Message_PostUser)\
            .filter(Message_PostUser.postid == post.id)\
            .filter(Message_PostUser.user_id == current_user.id)\
            .first()

        # getpost.unread = 0
        # db.session.add(getpost)

        howmanyusers = db.session\
            .query(Message_PostUser)\
            .filter_by(postid=post.id)\
            .count()

        if howmanyusers == 1:
            user1 = db.session\
                .query(Message_PostUser)\
                .filter_by(postid=post.id)\
                .order_by(Message_PostUser.timestamp.desc())\
                .limit(1)\
                .first()
            user2 = 0
            user3 = 0
        elif howmanyusers == 2:
            user1 = db.session\
                .query(Message_PostUser)\
                .filter_by(postid=post.id)\
                .order_by(Message_PostUser.timestamp.desc())\
                .limit(1)\
                .first()
            user2 = db.session\
                .query(Message_PostUser)\
                .filter_by(postid=post.id)\
                .order_by(Message_PostUser.timestamp.desc())\
                .limit(1)\
                .offset(1)\
                .first()
            user3 = 0
        elif howmanyusers == 3:
            user1 = db.session\
                .query(Message_PostUser)\
                .filter_by(postid=post.id)\
                .order_by(Message_PostUser.timestamp.desc())\
                .limit(1)\
                .offset(0)\
                .first()
            user2 = db.session\
                .query(Message_PostUser)\
                .filter_by(postid=post.id)\
                .order_by(Message_PostUser.timestamp.desc())\
                .limit(1)\
                .offset(1)\
                .first()
            user3 = db.session\
                .query(Message_PostUser)\
                .filter_by(postid=post.id)\
                .order_by(Message_PostUser.timestamp.desc())\
                .limit(1)\
                .offset(2)\
                .first()
        else:
            user1 = 0
            user2 = 0
            user3 = 0
            if howmanyusers > 3:
                user4 = db.session\
                    .query(Message_PostUser)\
                    .filter_by(postid=post.id)\
                    .order_by(Message_PostUser.timestamp.asc())\
                    .first()
                db.session.delete(user4)
                db.session.commit()
        comments = db.session\
            .query(Message_Comment)\
            .filter_by(post_id=post.id)\
            .order_by(Message_Comment.timestamp.desc())\
            .all()

        # sidebar stuff
        # Get New messages count
        allmsgcount = db.session\
            .query(Message_PostUser)\
            .filter(Message_PostUser.user_id == current_user.id)\
            .filter(Message_PostUser.unread == 1)\
            .count()

        # Get official Count
        officialmsgcount = db.session\
            .query(Message_PostUser)\
            .filter(Message_PostUser.user_id == current_user.id)\
            .filter(Message_PostUser.official == 1, Message_PostUser.dispute == 0, Message_PostUser.unread == 1)\
            .count()

        # Get Disputes Count
        disputesmsgcount = db.session\
            .query(Message_PostUser)\
            .filter(Message_PostUser.user_id == current_user.id)\
            .filter(Message_PostUser.dispute == 1)\
            .filter(Message_PostUser.unread == 1)\
            .count()

        # get read msg count
        oldmsgcount = db.session\
            .query(Message_PostUser)\
            .filter(Message_PostUser.user_id == current_user.id)\
            .filter(Message_PostUser.unread == 0)\
            .count()

        if request.method == 'POST':
            try:
                if form1.submit1.data and form1.validate_on_submit():
                    comment = Message_Comment(body=form1.msgplace.data,
                                              post_id=post.id,
                                              author=current_user.username,
                                              author_id=current_user.id,
                                              modid=0,
                                              timestamp=datetime.utcnow()
                                              )
                    db.session.add(comment)
                    db.session.flush()

                    getallposts = db.session\
                        .query(Message_PostUser)\
                        .filter(Message_PostUser.postid == post.id)\
                        .filter(Message_PostUser.user_id != current_user.id)\
                        .all()
                    for f in getallposts:
                        f.unread = 1
                        db.session.add(post)
                    db.session.commit()
                    flash('Your comment has been published.', category="success")
                    return redirect(url_for('message.message_post', id=post.id))
                elif form2.submit2.data and form2.validate_on_submit():
                    if howmanyusers <= 3:
                        if form2.adduserbody.data == "clearnet":
                            newpost = Message_PostUser(
                                # type of message
                                official=user1.official,
                                dispute=user1.dispute,
                                usermsg=user1.usermsg,
                                # info in msg
                                body=user1.body,
                                subject=user1.subject,
                                modid=0,
                                timestamp=now,
                                author_id=user1.author_id,
                                itemid=user1.itemid,
                                unread=1,

                                postid=post.id,
                                user_id=1,
                                username='Support'

                            )
                            db.session.add(newpost)
                            db.session.commit()
                            flash(
                                "support added to conversation.  Please wait for support to message. ", category="success")
                            return redirect(url_for('message.message_post', id=post.id))

                        elif form2.adduserbody.data == "Admin":
                            newpost2 = Message_PostUser(
                                official=user1.official,
                                dispute=user1.dispute,
                                usermsg=user1.usermsg,
                                body=user1.body,
                                subject=user1.subject,
                                timestamp=now,
                                author_id=user1.author_id,
                                itemid=user1.itemid,
                                unread=1,
                                modid=0,
                                postid=post.id,
                                user_id=1,
                                username='Support'
                            )
                            db.session.add(newpost2)
                            db.session.commit()
                            flash(
                                "support added to conversation.  Please wait for support to message. ", category="success")
                            return redirect(url_for('message.message_post', id=post.id))
                        else:
                            Usersearch = db.session\
                                .query(Auth_User)\
                                .filter_by(username=form2.adduserbody.data)\
                                .first()
                            if Usersearch is None:
                                flash("There is no user with the username " +
                                      form2.adduserbody.data, category="success")
                                return redirect(url_for('message.message_post', id=post.id))
                            else:
                                if howmanyusers <= 3:
                                    if user2 == 0:
                                        newpost3 = Message_PostUser(
                                            official=user1.official,
                                            dispute=user1.dispute,
                                            usermsg=user1.usermsg,
                                            body=user1.body,
                                            subject=user1.subject,
                                            timestamp=now,
                                            author_id=user1.author_id,
                                            itemid=user1.itemid,
                                            unread=1,
                                            modid=0,
                                            postid=post.id,
                                            user_id=Usersearch.id,
                                            username=Usersearch.username
                                        )
                                        notification(type=2,
                                                     username=Usersearch.username,
                                                     user_id=Usersearch.id,
                                                     salenumber=0,
                                                     bitcoin=0)
                                        flash("User added to conversation",
                                              category="success")
                                        db.session.add(newpost3)
                                        db.session.commit()
                                        return redirect(url_for('message.message_post', id=post.id))
                                    elif user3 == 0:
                                        newpost = Message_PostUser(
                                            # type of message
                                            official=user1.official,
                                            dispute=user1.dispute,
                                            usermsg=user1.usermsg,
                                            modid=0,
                                            body=user1.body,
                                            subject=user1.subject,
                                            timestamp=now,
                                            author_id=user1.author_id,
                                            itemid=user1.itemid,
                                            unread=1,
                                            postid=post.id,
                                            user_id=Usersearch.id,
                                            username=Usersearch.username
                                        )
                                        notification(type=2,
                                                     username=Usersearch.username,
                                                     user_id=Usersearch.id,
                                                     salenumber=0,
                                                     bitcoin=0)
                                        db.session.add(newpost)
                                        db.session.commit()
                                        flash("User added to conversation",
                                              category="success")
                                        return redirect(url_for('message.message_post', id=post.id))
                                    else:
                                        flash(
                                            "3 maximum users per conversation", category="success")
                                        return redirect(url_for('message.message_post', id=post.id))
                                else:
                                    flash("3 users max on a conversation",
                                          category="danger")
                                    return redirect(url_for('message.message_post', id=post.id))
                    else:
                        flash("3 users maximum", category="danger")
                        return redirect(url_for('message.message_post', id=post.id))
                else:
                    flash("Form Error", category="danger")
                    return redirect(url_for('message.message_post', id=post.id))
            except:
                return redirect(url_for('message.message_post', id=post.id))
        return render_template('messages/post.html',
                               post=post,
                               comments=comments,
                               now=now,
                               form1=form1,
                               form2=form2,
                               aform=aform,
                               disputesmsgcount=disputesmsgcount,
                               allmsgcount=allmsgcount,
                               officialmsgcount=officialmsgcount,
                               oldmsgcount=oldmsgcount,
                               user1=user1,
                               user2=user2,
                               user3=user3
                               )
    else:
        flash("Post doesnt exist", category="danger")
        return redirect(url_for('index'))


@message.route('/message_center-commentdelete/<int:id>', methods=['GET', 'POST'])
@login_required
def message_delete_comment(id):
    item = Message_Comment.query.get(id)
    if item:
        if item.author_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for('message.message_post', id=item.post_id))
        else:
            return redirect(url_for('index', username=current_user.username))
    else:
        flash("Post doesnt exist", category="danger")
        return redirect(url_for('index'))


def message_website_compose(personid, message, subject):
    now = datetime.utcnow()
    user = db.session\
        .query(Auth_User)\
        .filter_by(id=personid)\
        .first()
    if request.method == 'POST':
        # create postuser for author
        userpost2 = Message_PostUser(
            official=1,
            dispute=0,
            usermsg=0,
            body=message,
            subject=subject,
            timestamp=now,
            author_id=1,
            itemid=0,
            unread=1,
            modid=0,
            postid=0,
            user_id=user.id,
            username=user.username
        )

        notification(type=2,
                     username=user.username,
                     user_id=user.id,
                     salenumber=0,
                     bitcoin=0)
        db.session.add(userpost2)
        db.session.commit()
