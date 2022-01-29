import uuid
from pprint import pprint

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import current_app
from marshmallow import fields, Schema

from .resource import ListResource
from ext.api.base_schema import PagingSchema


def create_docs(resources: list) -> dict:
    spec = APISpec(
        **current_app.config['DOCS_CONFIG'],
        plugins=[MarshmallowPlugin()],
    )
    for resource in resources:
        if issubclass(resource, ListResource):
            class GetSchema(Schema):
                data = fields.Nested(resource.Schema, many=True)
                paging = fields.Nested(PagingSchema)

            # 注册GetSchema
            page_schema_name = f'{uuid.uuid4().hex}Schema'
            spec.components.schema(page_schema_name, schema=GetSchema)
            # 注册Post Schema
            post_schem_name = resource.PostSchema.__name__
            # spec.components.schema(post_schem_name, schema=resource.PostSchema)
            # 原本的schema
            schema_name = resource.Schema.__name__

            # 处理路径
            uri = resource.uri
            if '<string:parent_id>' in uri:
                uri = uri.replace('<string:parent_id>', '{' + f'{resource.Model.__name__}Id' + '}')

            spec.path(
                path=uri,
                operations=dict(
                    get=dict(
                        responses={"200": {"content": {"application/json": {"schema": page_schema_name}}}},
                        description=f"获取{resource.name}的列表"
                    ),
                    post=dict(
                        requestBody={"content": {"application/json": {"schema": post_schem_name}}},
                        responses={"200": {"content": {"application/json": {"schema": schema_name}}}},
                        description=f"创建{resource.name}"
                    )
                ),
            )
    pprint(spec.to_dict())
    return spec.to_dict()
