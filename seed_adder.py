from app.classes.models import Query_CategoryCats
from app import db
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only


def open_word_file():
    wordfile = "./word_seeds.txt"

    with open(wordfile) as word_file:
        valid_words = (word_file.read().split())
        thelist = (list(valid_words))

        for f in thelist:
            print(f)
            addwordtodb = Query_CategoryCats(text=f)
            db.session.add(addwordtodb)
        db.session.commit()


def get_words():
    get_words = db.session.query(
        Query_CategoryCats).order_by(func.random()).limit(5)
    for f in get_words:
        print(f.text)


get_words()
