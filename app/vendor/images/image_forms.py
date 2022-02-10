from ast import Pass
import os
from werkzeug.utils import secure_filename
from app import db
from flask_login import current_user
from app.vendor.images.item_image_resizer import imagespider
from app.common.functions import \
    id_generator_picture1, \
    id_generator_picture2, \
    id_generator_picture3, \
    id_generator_picture4, \
    id_generator_picture5, \
    itemlocation
from app import UPLOADED_FILES_DEST_ITEM
from app.classes.item import \
    marketItem

def deleteimg_noredirect(id, img):
    try:
        vendoritem = marketItem.query.get(id)
        if vendoritem:
            if vendoritem.vendor_id == current_user.id:
                try:
                    specific_folder = str(vendoritem.id)
                    getimagesubfolder = itemlocation(x=id)
                    spacer = '/'

                    pathtofile = str(UPLOADED_FILES_DEST_ITEM + spacer + getimagesubfolder + spacer + specific_folder + spacer + img)
                    file_extension=".jpg"
                    ext1 = '_225x'
                    ext2 = '_500x'
                    file0 = str(pathtofile + file_extension)
                    file1 = str(pathtofile + ext1 + file_extension)
                    file2 = str(pathtofile + ext2 + file_extension)

                    if len(img) > 20:

                        if vendoritem.imageone == img:
                            vendoritem.imageone = '0'
                            db.session.add(vendoritem)
                            db.session.commit()
                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif vendoritem.imagetwo == img:
                            vendoritem.imagetwo = '0'
                            db.session.add(vendoritem)
                            db.session.commit()
                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif vendoritem.imagethree == img:
                            vendoritem.imagethree = '0'
                            db.session.add(vendoritem)
                            db.session.commit()
                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif vendoritem.imagefour == img:
                            vendoritem.imagefour = '0'
                            db.session.add(vendoritem)
                            db.session.commit()
                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass

                        elif vendoritem.imagefive == img:
                            vendoritem.imagefive = '0'
                            db.session.add(vendoritem)
                            db.session.commit()
                            try:
                                os.remove(file0)
                            except Exception:
                                pass
                            try:
                                os.remove(file1)
                            except Exception:
                                pass
                        else:
                            pass
                except Exception:
                    pass
            else:
                pass
        else:
            pass
    except:
        pass

def image1(formdata, item, directoryifitemlisting):
    id_pic1 = id_generator_picture1()
    # if the form has an image
    if formdata:
        deleteimg_noredirect(id=item.id, img=item.imageone)
        filename = secure_filename(formdata.filename)
        # makes directory (generic location + auction number id as folder)
        # saves it to location
        imagepath = os.path.join(directoryifitemlisting, filename)
        formdata.save(imagepath)
        # split file name and ending
        filenamenew, file_extension = os.path.splitext(imagepath)
        # gets new 64 digit filenam
        newfileName = id_pic1 + file_extension
        # puts new name with ending
        filenamenewfull = filenamenew + file_extension
        # gets aboslute path of new file
        newfileNameDestination = os.path.join(directoryifitemlisting, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination)

        if len(formdata.filename) > 2:
            item.imageone = id_pic1
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            item.imageone = "0"
    else:
        # nothing no changes
        if len(item.imageone) > 5:
            pass
        else:
            # no image change to 0
            item.imageone = "0"


def image2(formdata, item, directoryifitemlisting):
    id_pic2 = id_generator_picture2()
    if formdata:
        deleteimg_noredirect(id=item.id, img=item.imagetwo)
        filename = secure_filename(formdata.filename)
        # makes directory (generic location + auction number id as folder)
        # saves it to location
        imagepath = os.path.join(directoryifitemlisting, filename)
        formdata.save(imagepath)
        # split file name and ending
        filenamenew, file_extension = os.path.splitext(imagepath)
        # gets new 64 digit filenam
        newfileName = id_pic2 + file_extension
        # puts new name with ending
        filenamenewfull = filenamenew + file_extension
        # gets aboslute path of new file
        newfileNameDestination2 = os.path.join(directoryifitemlisting, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination2)
        if len(formdata.filename) > 2:
            item.imagetwo = id_pic2
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            item.imagetwo = "0"
    else:
        if item.imagetwo:
            if len(item.imagetwo) > 5:
                pass
        else:
            item.imagetwo = "0"


def image3(formdata, item, directoryifitemlisting):
    id_pic3 = id_generator_picture3()
    if formdata:
        deleteimg_noredirect(id=item.id, img=item.imagethree)
        filename = secure_filename(formdata.filename)
        # makes directory (generic location + auction number id as folder)
        # saves it to location
        imagepath = os.path.join(directoryifitemlisting, filename)
        formdata.save(imagepath)
        # split file name and ending
        filenamenew, file_extension = os.path.splitext(
                            imagepath)
        # gets new 64 digit filenam
        newfileName = id_pic3 + file_extension
        # puts new name with ending
        filenamenewfull = filenamenew + file_extension
        # gets aboslute path of new file
        newfileNameDestination = os.path.join(directoryifitemlisting, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination)
        if len(formdata.filename) > 5:
            # add profile to db
            item.imagethree = id_pic3
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            item.imagethree = "0"

    else:
        if item.imagethree is not None:
            if len(item.imagethree) > 5:
                pass
        else:
            item.imagethree = "0"



def image4(formdata, item, directoryifitemlisting):
    id_pic4 = id_generator_picture4()
    if formdata:
        deleteimg_noredirect(id=item.id, img=item.imagefour)
        filename = secure_filename(formdata.filename)
        # makes directory (generic location + auction number id as folder)
        # saves it to location
        imagepath = os.path.join(directoryifitemlisting, filename)
        formdata.save(imagepath)
        # split file name and ending
        filenamenew, file_extension = os.path.splitext(imagepath)
        # gets new 64 digit filenam
        newfileName = id_pic4 + file_extension
        # puts new name with ending
        filenamenewfull = filenamenew + file_extension
        # gets aboslute path of new file
        newfileNameDestination = os.path.join(directoryifitemlisting, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination)
        if len(formdata.filename) > 2:
  
            # add profile to db
            item.imagefour = id_pic4
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            item.imagefour = "0"
    else:
        if item.imagefour:
            if len(item.imagefour) > 5:
                pass
        else:
            item.imagefour = "0"


def image5(formdata, item, directoryifitemlisting):
    id_pic5 = id_generator_picture5()
    if formdata:
        deleteimg_noredirect(id=item.id, img=item.imagefive)
        filename = secure_filename(formdata.filename)
        # makes directory (generic location + auction number id as folder)
        # saves it to location
        imagepath = os.path.join(directoryifitemlisting, filename)
        formdata.save(imagepath)
        # split file name and ending
        filenamenew, file_extension = os.path.splitext(imagepath)
        # gets new 64 digit filenam
        newfileName = id_pic5 + file_extension
        # puts new name with ending
        filenamenewfull = filenamenew + file_extension
        # gets aboslute path of new file
        newfileNameDestination = os.path.join(directoryifitemlisting, newfileName)
        # renames file
        os.rename(filenamenewfull, newfileNameDestination)
        if len(formdata.filename) > 2:

            # add profile to db
            item.imagefive = id_pic5
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            item.imagefive = "0"
    else:
        if item.imagefive:
            if len(item.imagefive) > 5:
                pass
        else:
            item.imagefive = "0"
