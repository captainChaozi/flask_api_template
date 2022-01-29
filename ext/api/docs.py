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

        schema_name = resource.Schema.__name__

        if issubclass(resource, ListResource):
            class GetSchema(Schema):
                data = fields.Nested(resource.Schema, many=True)
                paging = fields.Nested(PagingSchema)

            # 注册GetSchema
            page_schema_name = f'{uuid.uuid4().hex}Schema'
            spec.components.schema(page_schema_name, schema=GetSchema)
            post_schem_name = resource.PostSchema.__name__

            # 处理路径
            uri = resource.uri
            global_parameters = []
            # page
            page_parameter = {
                'in': 'query',
                'name': 'page',
                'schema': {
                    'type': 'integer'
                },
                'description': '第几页'
            }
            global_parameters.append(page_parameter)
            per_page_parameter = {
                'in': 'query',
                'name': 'per_page',
                'schema': {
                    'type': 'integer'
                },
                'description': '每页多少条'
            }
            global_parameters.append(per_page_parameter)
            if '<string:parent_id>' in uri:
                parameter_name = resource.parent_id_field
                uri = uri.replace('<string:parent_id>', '{' + parameter_name + '}')
                path_id_parameter = {
                    'in': 'path',
                    'name': parameter_name,
                    'schema': {
                        'type': 'string',
                    },

                }
                global_parameters.append(path_id_parameter)


            spec.path(
                path=uri,
                parameters=global_parameters,
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
        else:
            uri = resource.uri
            if '<string:resource_id>' in uri:
                uri = uri.replace('<string:resource_id>', '{' + f'{resource.Model.__name__}Id' + '}')
            put_schem_name = resource.PutSchema.__name__

            spec.path(
                path=uri,
                operations=dict(
                    get=dict(
                        responses={"200": {"content": {"application/json": {"schema": schema_name}}}},
                        description=f"获取单个{resource.name}"
                    ),
                    put=dict(
                        requestBody={"content": {"application/json": {"schema": put_schem_name}}},
                        responses={"200": {"content": {"application/json": {"schema": schema_name}}}},
                        description=f"修改{resource.name}"
                    )
                )
            )
    pprint(spec.to_dict())
    return spec.to_dict()
