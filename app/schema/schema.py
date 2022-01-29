from app.model import Author, Book
from ext import BaseSchema, MetaBase, PostMetaBase
from marshmallow import fields, Schema


class AuthorSchema(BaseSchema):
    name = fields.String(dump_only=True,)

    class Meta(MetaBase):
        model = Author


class AuthorPostSchema(BaseSchema):
    # name = fields.String(load_default='你好',dump_default='shijie',attribute='dddddd')

    class Meta(PostMetaBase):
        model = Author


class BookSchema(BaseSchema):
    author = fields.Nested(AuthorSchema)

    class Meta(MetaBase):
        model = Book
