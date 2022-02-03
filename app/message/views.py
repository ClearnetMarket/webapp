from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user
from app.message import message
from app import db

from app.message.forms import\
    addusertoconvoForm,\
    CommentForm,\
    sendmessageForm, \
    allActionForm,\
    topbuttonForm

# models
from app.classes.auth import User

from app.classes.message import \
    Post, \
    PostUser, \
    Comment

from app.notification import notification
from flask_paginate import Pagination, get_page_args
from datetime import datetime

from app.common.decorators import login_required, ping_user


@message.route('/messagecenter', methods=['GET', 'POST'])
@login_required
@ping_user
def messagecenter():
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    delormarkasread = topbuttonForm()
    title = 'Messages'

    # sidebar stuff
    # Get New messages count
    newmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.unread == 1)
    allmsgcount = newmsg.count()

    # get read msg count
    oldmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.unread == 0)
    oldmsgcount = oldmsg.count()

    # Get official Count
    officialmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.official == 1, PostUser.dispute == 0, PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # Get Disputes Count
    disputesmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.dispute == 1, PostUser.unread == 1)
    disputesmsgcount = disputesmsg.count()

    # Get all msgs for current page
    allmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.unread == 1)\
        .order_by(PostUser.timestamp.desc())

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
            specific_post = db.session.query(PostUser).filter_by(id=v).first()
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
        return redirect(url_for('message.messagecenter', username=current_user.username))

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


@message.route('/messagecenter-disputes', methods=['GET', 'POST'])
@login_required
@ping_user
def messagecenter_disputes():
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    delormarkasread = topbuttonForm()
    user = db.session\
        .query(User)\
        .filter_by(username=current_user.username)\
        .first()
    title = 'Disputes'

    # sidebar stuff
    # Get New messages count
    newmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.unread == 1)

    allmsgcount = newmsg.count()

    # Get official Count
    officialmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.official == 1, PostUser.dispute == 0, PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # get read msg count
    # get read msg count
    oldmsg = db.session.query(PostUser)
    oldmsg = oldmsg.filter(PostUser.user_id == current_user.id)
    oldmsg = oldmsg.filter(PostUser.unread == 0)

    oldmsgcount = oldmsg.count()
    # Get Disputes Count
    disputesmsg = db.session.query(PostUser)
    disputesmsg = disputesmsg.filter(PostUser.user_id == current_user.id)
    disputesmsg = disputesmsg.filter(PostUser.dispute == 1)
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
                    PostUser).filter_by(id=v).first()
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
            return redirect(url_for('message.messagecenter', username=current_user.username))
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
@ping_user
def messagecenter_oldmsgs():
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    delormarkasread = topbuttonForm()
    user = User.query.filter_by(username=current_user.username).first()
    title = 'Old Messages'

    # sidebar stuff
    # Get New messages count
    newmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.unread == 1)

    allmsgcount = newmsg.count()

    # Get official Count
    officialmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.official == 1, PostUser.dispute == 0, PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # Get Disputes Count
    disputesmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.dispute == 1)
    disputesmsgcount = disputesmsg.count()

    # get read msg count
    oldmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.unread == 0)\
        .order_by(PostUser.timestamp.desc())

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
                    PostUser).filter_by(id=v).first()
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
            return redirect(url_for('message.messagecenter', username=current_user.username))
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


@message.route('/messagecenter-official', methods=['GET', 'POST'])
@login_required
def messagecenter_official():
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    delormarkasread = topbuttonForm()
    user = db.session\
        .query(User)\
        .filter_by(username=current_user.username)\
        .first()
    title = 'Official Messages'

    # sidebar stuff
    # Get New messages count
    newmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.unread == 1)
    allmsgcount = newmsg.count()

    # get read msg count
    oldmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.unread == 0)
    oldmsgcount = oldmsg.count()

    # Get official Count
    officialmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.official == 1, PostUser.dispute == 0, PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # Get Disputes Count
    disputesmsg = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.dispute == 1, PostUser.unread == 1)
    disputesmsgcount = disputesmsg.count()

    # Get official Count
    officialmsginbox = db.session\
        .query(PostUser)\
        .filter(PostUser.user_id == current_user.id)\
        .filter(PostUser.official == 1, PostUser.dispute == 0)

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
                    PostUser).filter_by(id=v).first()
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
            return redirect(url_for('message.messagecenter', username=current_user.username))
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


@message.route('/messagecenter-sent', methods=['GET', 'POST'])
@login_required
def messagecenter_Sent():
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    delormarkasread = topbuttonForm()
    user = db.session\
        .query(User)\
        .filter_by(username=current_user.username)\
        .first()
    title = 'Sent'

    # sidebar stuff
    # Get New messages count
    newmsg = db.session.query(PostUser)
    newmsg = newmsg.filter(PostUser.user_id == current_user.id)
    newmsg = newmsg.filter(PostUser.unread == 1)

    allmsgcount = newmsg.count()

    # Get official Count
    officialmsg = db.session.query(PostUser)
    officialmsg = officialmsg.filter(PostUser.user_id == current_user.id)
    officialmsg = officialmsg.filter(
        PostUser.official == 1, PostUser.dispute == 0, PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # Get Disputes Count
    disputesmsg = db.session.query(PostUser)
    disputesmsg = disputesmsg.filter(
        PostUser.dispute == 1, PostUser.unread == 1)
    disputesmsgcount = disputesmsg.count()
    # get read msg count
    # get read msg count
    oldmsg = db.session.query(PostUser)
    oldmsg = oldmsg.filter(PostUser.user_id == current_user.id)
    oldmsg = oldmsg.filter(PostUser.unread == 0)
    oldmsgcount = oldmsg.count()

    # Get sent msgs
    sentmsg = db.session.query(PostUser)
    sentmsg = sentmsg.filter(PostUser.author_id == current_user.id)
    sentmsg = sentmsg.filter(PostUser.user_id == current_user.id)
    sentmsg = sentmsg.order_by(PostUser.timestamp.desc())

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
                    PostUser).filter_by(id=v).first()
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
            return redirect(url_for('message.messagecenter', username=current_user.username))
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


@message.route('/messagecenter-compose', methods=['GET', 'POST'])
@login_required
@ping_user
def messagecenter_Compose():
    now = datetime.utcnow()
    form = sendmessageForm(request.form)
    aform = allActionForm(request.form)

    user = User.query.filter_by(username=current_user.username).first()
    if user:
        pass
    else:
        flash("There is no user with the username " +
              form.username.data, category="danger")
        return redirect(url_for('message.messagecenter_Compose', username=current_user.username))
    title = 'Compose Message'

    # sidebar stuff
    # Get New messages count
    newmsg = db.session.query(PostUser)
    newmsg = newmsg.filter(PostUser.user_id == current_user.id)
    newmsg = newmsg.filter(PostUser.unread == 1)
    allmsgcount = newmsg.count()

    # Get official Count
    officialmsg = db.session.query(PostUser)
    officialmsg = officialmsg.filter(PostUser.user_id == current_user.id)
    officialmsg = officialmsg.filter(
        PostUser.official == 1, PostUser.dispute == 0, PostUser.unread == 1)
    officialmsgcount = officialmsg.count()

    # Get Disputes Count
    disputesmsg = db.session.query(PostUser)
    disputesmsg = disputesmsg.filter(PostUser.user_id == current_user.id)
    disputesmsg = disputesmsg.filter(
        PostUser.dispute == 1, PostUser.unread == 1)
    disputesmsgcount = disputesmsg.count()
    # get read msg count
    oldmsg = db.session.query(PostUser)
    oldmsg = oldmsg.filter(PostUser.user_id == current_user.id)
    oldmsg = oldmsg.filter(PostUser.unread == 1)

    oldmsgcount = oldmsg.count()

    if request.method == 'POST' and form.validate_on_submit():

        usersearch = db.session.query(User).filter_by(
            username=form.username.data).first()
        if usersearch is None:
            flash("There is no user with the username " +
                  form.username.data, category="success")
            return redirect(url_for('message.messagecenter_Compose', username=current_user.username))
        elif usersearch.username == current_user.username:
            flash("You cant send mail to yourself.", category="success")
            return redirect(url_for('message.messagecenter_Compose', username=current_user.username))
        else:

            newpost = Post(timestamp=now)
            db.session.add(newpost)

            db.session.flush()

            # create for person getting it
            userpost = PostUser(
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
            userpost2 = PostUser(
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

            return redirect(url_for('message.messagecenter', username=current_user.username))

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


@message.route('/messagecenter-compose-specific/<person>/', methods=['GET', 'POST'])
@login_required
@ping_user
def messagecenter_Compose_specificperson(person):
    now = datetime.utcnow()
    if current_user.admin > 0:
        return redirect(url_for('message.messagecenter_Compose_specificperson_admin', person=person))
    else:
        form = sendmessageForm(request.form)
        aform = allActionForm(request.form)
        user = db.session.query(User).filter_by(username=person).first()
        if user:
            # sidebar stuff
            # Get New messages count
            newmsg = db.session.query(PostUser)
            newmsg = newmsg.filter(PostUser.user_id == current_user.id)
            newmsg = newmsg.filter(PostUser.unread == 1)

            allmsgcount = newmsg.count()

            # Get official Count
            officialmsg = db.session.query(PostUser)
            officialmsg = officialmsg.filter(
                PostUser.user_id == current_user.id)
            officialmsg = officialmsg.filter(
                PostUser.official == 1, PostUser.dispute == 0, PostUser.unread == 1)
            officialmsgcount = officialmsg.count()

            # Get Disputes Count
            disputesmsg = db.session.query(PostUser)
            disputesmsg = disputesmsg.filter(
                PostUser.user_id == current_user.id)
            disputesmsg = disputesmsg.filter(
                PostUser.dispute == 1, PostUser.unread == 1)
            disputesmsgcount = disputesmsg.count()

            # get read msg count
            oldmsg = db.session.query(PostUser)
            oldmsg = oldmsg.filter(PostUser.user_id == current_user.id)
            oldmsg = oldmsg.filter(PostUser.unread == 1)

            oldmsgcount = oldmsg.count()

            if request.method == 'POST':
                if form.validate_on_submit():

                    post = Post(
                        timestamp=now
                    )
                    db.session.add(post)
                    db.session.flush()

                    # create postuser for author
                    userpost2 = PostUser(
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
                    userpost = PostUser(
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
                    return redirect(url_for('message.messagecenter', username=current_user.username))

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
            return redirect(url_for('message.messagecenter', username=current_user.username))


@message.route('/messagecenter-compose-specific-admin/<person>/', methods=['GET', 'POST'])
@login_required
@ping_user
def messagecenter_Compose_specificperson_admin(person):
    now = datetime.utcnow()

    if current_user.admin == 0:
        return redirect(url_for('index'))
    else:
        form = sendmessageForm(request.form)
        aform = allActionForm(request.form)
        user = db.session.query(User).filter_by(username=person).first()
        if user:
            # sidebar stuff
            # Get New messages count
            newmsg = db.session.query(PostUser)
            newmsg = newmsg.filter(PostUser.user_id == current_user.id)
            newmsg = newmsg.filter(PostUser.unread == 1)

            allmsgcount = newmsg.count()

            # Get official Count
            officialmsg = db.session.query(PostUser)
            officialmsg = officialmsg.filter(
                PostUser.user_id == current_user.id)
            officialmsg = officialmsg.filter(
                PostUser.official == 1, PostUser.dispute == 0, PostUser.unread == 1)
            officialmsgcount = officialmsg.count()

            # Get Disputes Count
            disputesmsg = db.session.query(PostUser)
            disputesmsg = disputesmsg.filter(
                PostUser.user_id == current_user.id)
            disputesmsg = disputesmsg.filter(
                PostUser.dispute == 1, PostUser.unread == 1)
            disputesmsgcount = disputesmsg.count()

            # get read msg count
            oldmsg = db.session.query(PostUser)
            oldmsg = oldmsg.filter(PostUser.user_id == current_user.id)
            oldmsg = oldmsg.filter(PostUser.unread == 0)

            oldmsgcount = oldmsg.count()
            if request.method == 'POST':

                try:
                    newpost = Post(
                        timestamp=now
                    )
                    db.session.add(newpost)
                    db.session.flush()

                    # create postuser for author
                    userpost2 = PostUser(
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
                    userpost = PostUser(
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
                    return redirect(url_for('message.messagecenter'))
                except:
                    db.session.rollback()
                    flash("Form Error", category="danger")
                    return redirect(url_for('message.messagecenter_Compose_specificperson', person=current_user.username))
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
            return redirect(url_for('message.messagecenter', username=current_user.username))


@message.route('/post/<int:id>', methods=['GET', 'POST'])
@login_required
def post(id):
    now = datetime.utcnow()
    aform = allActionForm(request.form)
    form1 = CommentForm(request.form)
    form2 = addusertoconvoForm(request.form)
    post = db.session\
        .query(Post)\
        .filter_by(id=id)\
        .first()
    if post:
        getpost = db.session\
            .query(PostUser)\
            .filter(PostUser.postid == post.id)\
            .filter(PostUser.user_id == current_user.id)\
            .first()

        # getpost.unread = 0
        # db.session.add(getpost)

        howmanyusers = db.session\
            .query(PostUser)\
            .filter_by(postid=post.id)\
            .count()

        if howmanyusers == 1:
            user1 = db.session\
                .query(PostUser)\
                .filter_by(postid=post.id)\
                .order_by(PostUser.timestamp.desc())\
                .limit(1)\
                .first()
            user2 = 0
            user3 = 0
        elif howmanyusers == 2:
            user1 = db.session\
                .query(PostUser)\
                .filter_by(postid=post.id)\
                .order_by(PostUser.timestamp.desc())\
                .limit(1)\
                .first()
            user2 = db.session\
                .query(PostUser)\
                .filter_by(postid=post.id)\
                .order_by(PostUser.timestamp.desc())\
                .limit(1)\
                .offset(1)\
                .first()
            user3 = 0
        elif howmanyusers == 3:
            user1 = db.session\
                .query(PostUser)\
                .filter_by(postid=post.id)\
                .order_by(PostUser.timestamp.desc())\
                .limit(1)\
                .offset(0)\
                .first()
            user2 = db.session\
                .query(PostUser)\
                .filter_by(postid=post.id)\
                .order_by(PostUser.timestamp.desc())\
                .limit(1)\
                .offset(1)\
                .first()
            user3 = db.session\
                .query(PostUser)\
                .filter_by(postid=post.id)\
                .order_by(PostUser.timestamp.desc())\
                .limit(1)\
                .offset(2)\
                .first()
        else:
            user1 = 0
            user2 = 0
            user3 = 0
            if howmanyusers > 3:
                user4 = db.session\
                    .query(PostUser)\
                    .filter_by(postid=post.id)\
                    .order_by(PostUser.timestamp.asc())\
                    .first()
                db.session.delete(user4)
                db.session.commit()
        comments = db.session\
            .query(Comment)\
            .filter_by(post_id=post.id)\
            .order_by(Comment.timestamp.desc())\
            .all()

        # sidebar stuff
        # Get New messages count
        allmsgcount = db.session\
            .query(PostUser)\
            .filter(PostUser.user_id == current_user.id)\
            .filter(PostUser.unread == 1)\
            .count()

        # Get official Count
        officialmsgcount = db.session\
            .query(PostUser)\
            .filter(PostUser.user_id == current_user.id)\
            .filter(PostUser.official == 1, PostUser.dispute == 0, PostUser.unread == 1)\
            .count()

        # Get Disputes Count
        disputesmsgcount = db.session\
            .query(PostUser)\
            .filter(PostUser.user_id == current_user.id)\
            .filter(PostUser.dispute == 1)\
            .filter(PostUser.unread == 1)\
            .count()

        # get read msg count
        oldmsgcount = db.session\
            .query(PostUser)\
            .filter(PostUser.user_id == current_user.id)\
            .filter(PostUser.unread == 0)\
            .count()

        if request.method == 'POST':
            try:
                if form1.submit1.data and form1.validate_on_submit():
                    comment = Comment(body=form1.msgplace.data,
                                      post_id=post.id,
                                      author=current_user.username,
                                      author_id=current_user.id,
                                      modid=0,
                                      timestamp=datetime.utcnow()
                                      )
                    db.session.add(comment)
                    db.session.flush()

                    getallposts = db.session\
                        .query(PostUser)\
                        .filter(PostUser.postid == post.id)\
                        .filter(PostUser.user_id != current_user.id)\
                        .all()
                    for f in getallposts:
                        f.unread = 1
                        db.session.add(post)
                    db.session.commit()
                    flash('Your comment has been published.', category="success")
                    return redirect(url_for('message.post', id=post.id))
                elif form2.submit2.data and form2.validate_on_submit():
                    if howmanyusers <= 3:
                        if form2.adduserbody.data == "clearnet":
                            newpost = PostUser(
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
                            return redirect(url_for('message.post', id=post.id))

                        elif form2.adduserbody.data == "Admin":
                            newpost2 = PostUser(
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
                            return redirect(url_for('message.post', id=post.id))
                        else:
                            Usersearch = db.session\
                                .query(User)\
                                .filter_by(username=form2.adduserbody.data)\
                                .first()
                            if Usersearch is None:
                                flash("There is no user with the username " +
                                      form2.adduserbody.data, category="success")
                                return redirect(url_for('message.post', id=post.id))
                            else:
                                if howmanyusers <= 3:
                                    if user2 == 0:
                                        newpost3 = PostUser(
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
                                        return redirect(url_for('message.post', id=post.id))
                                    elif user3 == 0:
                                        newpost = PostUser(
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
                                        return redirect(url_for('message.post', id=post.id))
                                    else:
                                        flash(
                                            "3 maximum users per conversation", category="success")
                                        return redirect(url_for('message.post', id=post.id))
                                else:
                                    flash("3 users max on a conversation",
                                          category="danger")
                                    return redirect(url_for('message.post', id=post.id))
                    else:
                        flash("3 users maximum", category="danger")
                        return redirect(url_for('message.post', id=post.id))
                else:
                    flash("Form Error", category="danger")
                    return redirect(url_for('message.post', id=post.id))
            except:
                return redirect(url_for('message.post', id=post.id))
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


@message.route('/messagecenter-commentdelete/<int:id>', methods=['GET', 'POST'])
@login_required
def messagecenter_delete_comment(id):
    item = Comment.query.get(id)
    if item:
        if item.author_id == current_user.id:
            db.session.delete(item)
            db.session.commit()
            return redirect(url_for('message.post', id=item.post_id))
        else:
            return redirect(url_for('index', username=current_user.username))
    else:
        flash("Post doesnt exist", category="danger")
        return redirect(url_for('index'))


def messagecenter_WEBSITEcompose(personid, message, subject):
    now = datetime.utcnow()
    user = db.session\
        .query(User)\
        .filter_by(id=personid)\
        .first()
    if request.method == 'POST':
        # create postuser for author
        userpost2 = PostUser(
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
