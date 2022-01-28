import uuid

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

            page_schema_name = f'{uuid.uuid4().hex}Schema'
            spec.components.schema(page_schema_name, schema=GetSchema)
            schema_name = resource.Schema.__name__

            spec.path(
                path=f"{resource.uri}",
                operations=dict(
                    get=dict(
                        # parameters=[{} fro i in resource.],
                        responses={"200": {"content": {"application/json": {"schema": page_schema_name}}}},
                        description=f"获取{resource.name}的列表"
                    ),
                    post=dict(
                        responses={"200": {"content": {"application/json": {"schema": schema_name}}}},
                        description=f"创建{resource.name}"
                    )
                ),
            )

    return spec.to_dict()
