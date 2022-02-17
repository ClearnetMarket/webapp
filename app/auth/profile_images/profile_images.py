from flask_login import current_user, logout_user, login_user
from app import db, UPLOADED_FILES_DEST_USER
from app.auth.profile_images.profile_image_resizer import imagespider
from flask import redirect, url_for
from werkzeug.utils import secure_filename
import os
from app.common.functions import id_generator_picture1

from app.classes.auth import Auth_User
from app.common.functions import mkdir_p


def deleteprofileimage(id, img, type):
    if current_user.id == id:
        user = db.session \
            .query(Auth_User)\
            .filter(Auth_User.id == id)\
            .first()
        user_id = str(id)
        # img name in database
        userimg1 = str(img) + '.jpg'
        # remove extension and jpg
        userimg2 = str(img) + '_125x.jpg'
        usernodelocation = str(user.usernode)
        file0 = os.path.join(UPLOADED_FILES_DEST_USER,
                             usernodelocation, user_id, userimg1)
        file1 = os.path.join(UPLOADED_FILES_DEST_USER,
                             usernodelocation, user_id, userimg2)
        try:
            os.remove(file0)
            os.remove(file1)
        except Exception:
            user.profileimage = 'user-unknown.png'
            db.session.add(user)
            db.session.commit()
        if type == 0:
            pass
        elif type == 1:
            user.profileimage = 'user-unknown.png'
            db.session.add(user)
            db.session.commit()
        else:
            pass
    else:
        return redirect(url_for('index'))


def image1(formdata, directoryifitemlisting, user):
    # type decides if change username or not
    id_pic1 = id_generator_picture1()
    # make a directory
    mkdir_p(path=directoryifitemlisting)
    # delete profile image type 0 since we dont change name
    deleteprofileimage(id=current_user.id,
                       img=current_user.profileimage, type=0)
    # secure the filename
    filename = secure_filename(formdata.filename)
    # saves it to location
    profileimagefilepath = os.path.join(directoryifitemlisting, filename)
    # add the save folder
    formdata.save(profileimagefilepath)
    # rename file
    # split file name and ending
    filenamenew, file_extension = os.path.splitext(profileimagefilepath)
    # gets new 64 digit filename
    newfileName = id_pic1 + file_extension
    # puts new name with ending
    filenamenewfull = filenamenew + file_extension
    # gets aboslute path of new file
    newfileNameDestination = os.path.join(directoryifitemlisting, newfileName)
    # renames file
    os.rename(filenamenewfull, newfileNameDestination)

    # add user entry to profile image
    if formdata.filename:
        db_entry = id_pic1
        # add profile to db
        user.profileimage = db_entry
        db.session.add(user)
    else:
        db_entry = "user-unknown.png"
    # change image size
    imagespider(base_path=directoryifitemlisting)
    return db_entry
