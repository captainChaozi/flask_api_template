from app import Author, Book
from ext import MainSchema, MetaBase
from marshmallow import fields,Schema

class PagingSchema(Schema):
    page = fields.Integer()
    per_page = fields.Integer()
    total_number = fields.Integer()



class AuthorSchema(MainSchema):
    class Meta(MetaBase):
        model = Author

class AuthorGetSchema(Schema):
    data = fields.Nested(AuthorSchema,many=True)
    paging = fields.Nested(PagingSchema)


class BookSchema(MainSchema):
    author = fields.Nested(AuthorSchema)

    class Meta(MetaBase):
        model = Book
