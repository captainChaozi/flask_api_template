import uuid
from pprint import pprint

from apispec import APISpec
from copy import deepcopy
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import current_app
from marshmallow import fields, Schema
from .resource import ListResource, DetailResource
from ext.api.base_schema import PagingSchema, IDSchema
from sqlalchemy import String, Integer, Date


class MyAPISpec(object):

    def __init__(self):
        self.spec = APISpec(
            **current_app.config['DOCS_CONFIG'],
            plugins=[MarshmallowPlugin()], )
        self.operations = dict()

    @staticmethod
    def path(url, *parameter_names):
        old = url[url.find('<'):url.find('>') + 1]
        for parameter_name in parameter_names:
            url = url.replace(old, '{' + parameter_name + '}')
        return url

    @staticmethod
    def add_parameter(name, _in, _type, require=False, default=None, describe=None):
        data = {
            'in': _in,
            'name': name,
            'schema': {
                'type': _type,
            },
            'required': require
        }
        if default is not None:
            data['schema']['default'] = default
        if describe:
            data['describe'] = describe
        return data

    @staticmethod
    def request_body(schema):
        return {"content": {"application/json": {"schema": schema}}}

    @staticmethod
    def response(schema=None, status="200", description='ok'):
        content = {"description": description}
        if schema:
            content['application/json'] = {"schema": schema}
        return {status: content}

    def get_opt(self, description, parameters=None, *response):
        response_data = dict()
        for i in response:
            response_data.update(i)

        self.operations['get'] = {
            'parameters': parameters if parameters else [],
            'responses': response_data,
            'description': description
        }

    def put_opt(self, description, request, *response):
        response_data = dict()
        for i in response:
            response_data.update(i)
        self.operations['put'] = {
            'requestBody': request,
            'responses': response_data,
            'description': description
        }

    def post_opt(self, description, request, *response):
        response_data = dict()
        for i in response:
            response_data.update(i)
        self.operations['post'] = {
            'requestBody': request,
            'responses': response_data,
            'description': description
        }

    def delete_opt(self, description, request=None, *response):
        response_data = dict()
        for i in response:
            response_data.update(i)
        data = {
            'responses': response_data,
            'description': description
        }
        if request:
            data['requestBody'] = request
        self.operations['delete'] = data

    def docs_create(self, path, parameters=None):
        self.spec.path(
            path=path,
            parameters=parameters if parameters else [],
            operations=deepcopy(self.operations)
        )
        self.operations.clear()

    def to_dict(self):
        return self.spec.to_dict()

    def list_docs(self, resource):

        global_parameters = []
        path = resource.uri
        if '<string:parent_id>' in path:
            path = self.path(path, resource.parent_id_field)
            global_parameters.append(self.add_parameter(resource.parent_id_field,
                                                        _in='path',
                                                        _type='string',
                                                        require=True,
                                                        ))
        get_parameters = []

        # page
        get_parameters.append(self.add_parameter('page', 'query', 'integer', default=1, describe='第几页'))
        get_parameters.append(self.add_parameter('per_page', 'query', 'integer', default=10, describe='每页多少条'))

        # 配置get的查询参数
        # between field
        for i in resource.between_field:
            get_parameters.append(self.add_parameter(i + '_start', 'query', 'string'))
            get_parameters.append(self.add_parameter(i + '_end', 'query', 'string'))
        # search 字段
        if resource.search_field:
            get_parameters.append(self.add_parameter('search', 'query', 'string'))
        # 其他字段单独查询
        for name, column in resource.Model.__table__.columns.items():
            column_class = column.type.__class__
            if column_class in [String, Date, Integer] and name not in ['id', 'is_delete']:

                if column_class == String:
                    _type = 'string'
                elif column_class == Date:
                    _type = 'date'
                else:
                    _type = 'integer'
                get_parameters.append(self.add_parameter(name, 'query', _type))

        class GetSchema(Schema):
            data = fields.Nested(resource.Schema, many=True)
            paging = fields.Nested(PagingSchema)

        get_schema_name = f'{uuid.uuid4().hex}Schema'

        self.spec.components.schema(get_schema_name, schema=GetSchema)

        # self.schema_register(get_schema_name, GetSchema)
        get_response = self.response(get_schema_name)
        self.get_opt(f"获取{resource.name}的列表", get_parameters, get_response)
        request = self.request_body(resource.PostSchema.__name__)
        response = self.response(resource.Schema.__name__)
        self.post_opt(f"创建{resource.name}", request, response)
        delete_request = self.request_body(IDSchema.__name__)
        delete_response = self.response(description='删除成功')
        self.delete_opt(f"批量删除{resource.name}", delete_request, delete_response)
        self.docs_create(path=path, parameters=global_parameters)

    def detail_docs(self, resource):

        path_parameter_name = f'{resource.Model.__name__}Id'
        path = self.path(resource.uri, path_parameter_name)
        path_id_parameter = self.add_parameter(path_parameter_name, 'path', 'string', require=True)
        get_response = self.response(resource.Schema.__name__)
        self.get_opt(f"创建{resource.name}", None, get_response)
        put_request = self.request_body(resource.PutSchema.__name__)
        put_response = self.response(resource.Schema.__name__)
        self.put_opt(f"修改{resource.name}", put_request, put_response)
        delete_response = self.response(description='删除成功')
        self.delete_opt(f"删除{resource.name}", None, delete_response)
        self.docs_create(path=path, parameters=[path_id_parameter])

    def common_docs(self, resources):
        for resource in resources:
            if issubclass(resource, ListResource):
                self.list_docs(resource)
            else:
                self.detail_docs(resource)
        return self.to_dict()
