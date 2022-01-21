from app.ext_init import db
from ext import MainMixIn


class Author(db.Model, MainMixIn):
    name = db.Column(db.String(50))
    birth = db.Column(db.Date)


class Book(db.Model, MainMixIn):
    name = db.Column(db.String(50))
    author_id = db.Column(db.ForeignKey('author.id'))
    author = db.relationship('Author', backref = db.backref('books'))
