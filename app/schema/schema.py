from app.model import Author, Book
from ext import BaseSchema, MetaBase, PostMetaBase
from marshmallow import fields


class AuthorSchema(BaseSchema):

    class Meta(MetaBase):
        model = Author


class AuthorPostSchema(BaseSchema):
    class Meta(PostMetaBase):
        model = Author


class BookSchema(BaseSchema):
    author = fields.Nested(AuthorSchema)

    class Meta(MetaBase):
        model = Book


class BookPostSchema(BaseSchema):

    class Meta(PostMetaBase):
        model = Book
