from app.model import Author, Book
from app.schema.schema import AuthorSchema, BookSchema, AuthorPostSchema, BookPostSchema
from ext import ListResource, DetailResource
from app.ext_init import docs


class AuthorListResource(ListResource):
    name = '作者'
    uri = '/author'
    docs = docs
    Model = Author
    Schema = AuthorSchema
    PostSchema = AuthorPostSchema
    between_field = ('create_time','modify_time')
    search_field = ('name',)


class AuthorDetailResource(DetailResource):
    name = '作者'
    uri = '/author/<string:resource_id>'
    docs = docs
    Model = Author
    Schema = AuthorSchema
    PutSchema = AuthorPostSchema


class BookListResource(ListResource):
    name = '书本'
    uri = '/author/<string:parent_id>/books'
    docs = docs
    Model = Book
    Schema = BookSchema
    PostSchema = BookPostSchema
    parent_id_field = 'author_id'


class BookDetailResource(DetailResource):
    name = '书本'
    uri = '/book/<string:resource_id>'
    docs = docs
    Model = Book
    Schema = BookSchema
    PutSchema = BookPostSchema
