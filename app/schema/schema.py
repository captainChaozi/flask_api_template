from app.model import Author, Book
from ext import MainSchema, MetaBase
from marshmallow import fields, Schema


class AuthorSchema(MainSchema):
    class Meta(MetaBase):
        model = Author



class BookSchema(MainSchema):
    author = fields.Nested(AuthorSchema)

    class Meta(MetaBase):
        model = Book
