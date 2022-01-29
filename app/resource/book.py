from app.model import Author, Book
from app.schema.schema import AuthorSchema, BookSchema, AuthorPostSchema
from ext import ListResource


class AuthorListResource(ListResource):
    name = '作者'
    uri = '/author/'
    Model = Author
    Schema = AuthorSchema
    PostSchema = AuthorPostSchema


class BookListResource(ListResource):
    name = '书本'
    uri = '/author/<string:parent_id>/books'
    Model = Book
    Schema = BookSchema
    PostSchema = AuthorPostSchema
