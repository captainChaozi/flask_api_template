from app.model import Author, Book
from app.schema.schema import AuthorSchema, BookSchema, AuthorPostSchema, BookPostSchema
from ext import ListResource, DetailResource


class AuthorListResource(ListResource):
    name = '作者'
    uri = '/author'
    Model = Author
    Schema = AuthorSchema
    PostSchema = AuthorPostSchema


class AuthorDetailResource(DetailResource):
    name = '作者'
    uri = '/author/<string:resource_id>'
    Model = Author
    Schema = AuthorSchema
    PutSchema = AuthorPostSchema


class BookListResource(ListResource):
    name = '书本'
    uri = '/author/<string:parent_id>/books'
    Model = Book
    Schema = BookSchema
    PostSchema = BookPostSchema
    parent_id_field = 'author_id'


class BookDetailResource(DetailResource):
    name = '书本'
    uri = '/book/<string:resource_id>'
    Model = Book
    Schema = BookSchema
    PostSchema = BookPostSchema
