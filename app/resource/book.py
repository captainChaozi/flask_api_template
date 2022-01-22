from flask_apispec import MethodResource, marshal_with, use_kwargs, doc
from flask import g
from marshmallow import fields

from ext import paginator
from app import Author
from app.schema.schema import AuthorSchema, PagingSchema, AuthorGetSchema
from ext import ListResource

@doc(description='a pet store', tags=['pets'])
class AuthorListResource(MethodResource):

    @use_kwargs({'category': fields.Str(), 'size': fields.Str()},location='args',apply=False)
    @marshal_with(AuthorGetSchema,code=200,description='获取单个Author',apply=False)
    def get(self):
        schema = AuthorSchema(many=True)
        query = g.db_session.query(Author)
        return paginator(query,schema)



