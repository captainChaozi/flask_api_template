
from app import Author
from app.schema.schema import AuthorSchema
from ext import ListResource

class AuthorListResource(ListResource):
    Model = Author
    Schema = AuthorSchema