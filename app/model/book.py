from app.ext_init import db
from ext import BaseMixIn


class Author(db.Model, BaseMixIn):
    name = db.Column(db.String(50), nullable=False,comment='作者名称')
    birth = db.Column(db.Date)


class Book(db.Model, BaseMixIn):
    name = db.Column(db.String(50))
    author_id = db.Column(db.ForeignKey('author.id'))
    author = db.relationship('Author', backref=db.backref('books'))


class Pet(db.Model, BaseMixIn):
    name = db.Column(db.String(50))
    category = db.Column(db.Integer)
    size = db.Column(db.String(20))
