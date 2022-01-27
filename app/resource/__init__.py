from ext.base_schema import PagingSchema
from .book import AuthorListResource, BookListResource
from marshmallow import Schema, fields
import inspect
import uuid
import sys
from flask_restful import Api
from apispec import APISpec
from config import docs_file
from ext import ListResource


def resource_register(api: Api, spec: APISpec):
    for _, resource in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if issubclass(resource, ListResource) and resource != ListResource:
            api.add_resource(resource, resource.uri)

            class GetSchema(Schema):
                data = fields.Nested(resource.Schema, many=True)
                paging = fields.Nested(PagingSchema)

            page_schema_name = f'{uuid.uuid4().hex}Schema'
            spec.components.schema(page_schema_name, schema=GetSchema)
            schema_name = resource.Schema.__name__
            # spec.components.schema(schema_name,schema=resource.Schema)

            spec.path(
                path=f"{resource.uri}",
                operations=dict(
                    get=dict(
                        responses={"200": {"content": {"application/json": {"schema": page_schema_name}}}},
                        description=f"获取{resource.name}的列表"
                    ),
                    post=dict(
                        responses={"200": {"content": {"application/json": {"schema": schema_name}}}},
                        description=f"创建{resource.name}"
                    )
                ),
            )
    with open(docs_file, 'w') as f:
        f.write(spec.to_yaml())
