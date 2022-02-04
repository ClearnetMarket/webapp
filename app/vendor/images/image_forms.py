from ast import Pass
import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
from app import db
from flask_login import current_user
from app.vendor.images.item_image_resizer import imagespider
from app.common.functions import \
    id_generator_picture1, \
    id_generator_picture2, \
    id_generator_picture3, \
    id_generator_picture4, \
    id_generator_picture5
from app import UPLOADED_FILES_DEST
from app.classes.item import \
    marketItem

def deleteimg_noredirect(id, img):
    try:
        vendoritem = marketItem.query.get(id)
        if vendoritem:
            if vendoritem.vendor_id == current_user.id:
                try:
                    specific_folder = str(vendoritem.id)

                    link = 'listing'
                    spacer = '/'
                    pathtofile = str(UPLOADED_FILES_DEST + link +
                                     spacer + specific_folder + spacer + img)
                    pathtofile, file_extension = os.path.splitext(pathtofile)

                    ext1 = '_225x'

                    file0 = str(pathtofile + file_extension)
                    file1 = str(pathtofile + ext1 + file_extension)

                    if len(img) > 20:
                        x1 = vendoritem.imageone
                        x2 = vendoritem.imagetwo
                        x3 = vendoritem.imagethree
                        x4 = vendoritem.imagefour
                        x5 = vendoritem.imagefive

                        if x1 == img:
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

                        elif x2 == img:
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

                        elif x3 == img:
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

                        elif x4 == img:
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

                        elif x5 == img:
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
    except:
        pass

def image1(formdata, item, directoryifitemlisting):
    id_pic1 = id_generator_picture1()
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
            x1 = newfileName
            item.imageone = id_pic1
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            x1 = "0"
        return x1
    else:
        if len(item.imageone) > 5:
            pass
        else:
            x1 = "0"
            return x1


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
            x2 = newfileName
            item.imagetwo = id_pic2
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            x2 = "0"
        return x2
    else:
        if item.imagetwo:
            if len(item.imagetwo) > 5:
                pass
        else:
            x2 = "0"
            return x2


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
        if len(formdata.filename) > 2:
            x3 = newfileName
            # add profile to db
            item.imagethree = id_pic3
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            x3 = "0"
        return x3
    else:
        if item.imagetwo:
            if len(item.imagethree) > 5:
                pass
        else:
            x3 = "0"
            return x3


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
            x4 = newfileName
            # add profile to db
            item.imagefour = id_pic4
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            x4 = "0"
        return x4
    else:
        if item.imagefour:
            if len(item.imagefour) > 5:
                pass
        else:
            x4 = "0"
            return x4


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
            x5 = newfileName
            # add profile to db
            item.imagefive = id_pic5
            db.session.add(item)
            imagespider(base_path=directoryifitemlisting)
        else:
            x5 = "0"
        return x5
    else:
        if item.imagefive:
            if len(item.imagefive) > 5:
                pass
        else:
            x5 = "0"
            return x5
