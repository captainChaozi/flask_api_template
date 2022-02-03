import uuid

from apispec import APISpec
from copy import deepcopy
from apispec.ext.marshmallow import MarshmallowPlugin
from marshmallow import fields, Schema
from ext.api.base_schema import PagingSchema, IDSchema
from sqlalchemy import String, Integer, Date


class Docs(object):

    def __init__(self, app=None):
        self.spec = None
        self.operations_data = dict()
        self.parameters_data = []
        self.request_body_data = dict()
        self.response_data = dict()
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.spec = APISpec(
            **app.config['DOCS_CONFIG'],
            plugins=[MarshmallowPlugin()], )

    @staticmethod
    def path(url, *parameter_names):
        old = url[url.find('<'):url.find('>') + 1]
        for parameter_name in parameter_names:
            url = url.replace(old, '{' + parameter_name + '}')
        return url

    def parameter(self, name, _in, _type, require=False, default=None, describe=None):
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
        self.parameters_data.append(data)

    def request_body(self, schema):
        self.request_body_data = {"content": {"application/json": {"schema": schema}}}

    def response(self, schema=None, status="200", description='ok'):
        content = {"description": description}
        if isinstance(schema, str):
            content['content'] = {'application/json': {"schema": schema}}
        self.response_data[status] = content

    def get_opt(self, description, tags=None):

        self.operations_data['get'] = {
            'parameters': deepcopy(self.parameters_data),
            'responses': deepcopy(self.response_data),
            'description': description,
            "tags": tags if tags else []
        }
        self.parameters_data.clear()
        self.response_data.clear()

    def put_opt(self, description, tags=None):

        self.operations_data['put'] = {
            'parameters': deepcopy(self.parameters_data),
            'requestBody': deepcopy(self.request_body_data),
            'responses': deepcopy(self.response_data),
            'description': description,
            "tags": tags if tags else []

        }
        self.parameters_data.clear()
        self.request_body_data.clear()
        self.response_data.clear()

    def post_opt(self, description, tags=None):

        self.operations_data['post'] = {
            'parameters': deepcopy(self.parameters_data),
            'requestBody': deepcopy(self.request_body_data),
            'responses': deepcopy(self.response_data),
            'description': description,
            "tags": tags if tags else []

        }
        self.parameters_data.clear()
        self.request_body_data.clear()
        self.response_data.clear()

    def delete_opt(self, description, tags=None):

        data = {
            'parameters': deepcopy(self.parameters_data),
            'responses': deepcopy(self.response_data),
            'description': description,
            "tags": tags if tags else []

        }
        if self.request_body_data:
            data['requestBody'] = deepcopy(self.request_body_data)
        self.operations_data['delete'] = data
        self.parameters_data.clear()
        self.request_body_data.clear()
        self.response_data.clear()

    def create(self, path):
        self.spec.path(
            path=path,
            operations=deepcopy(self.operations_data),
        )
        self.operations_data.clear()

    def to_dict(self):
        return self.spec.to_dict()

    def list_docs(self, resource):
        class GetSchema(Schema):
            data = fields.Nested(resource.Schema, many=True)
            paging = fields.Nested(PagingSchema)

        get_schema_name = f'{uuid.uuid4().hex}Schema'

        self.spec.components.schema(get_schema_name, schema=GetSchema)
        # page
        self.parameter('page', 'query', 'integer', default=1, describe='第几页')
        self.parameter('per_page', 'query', 'integer', default=10, describe='每页多少条')

        # 配置get的查询参数
        # between field
        for i in resource.between_field:
            self.parameter(i + '_start', 'query', 'string')
            self.parameter(i + '_end', 'query', 'string')
        # search 字段
        if resource.search_field:
            self.parameter('search', 'query', 'string')
        # 其他字段单独查询
        for name, column in resource.Model.__table__.columns.items():
            column_class = column.type.__class__
            if column_class in [String, Date, Integer] and name not in ['id', 'is_delete']:
                if name in resource.equal_field or name in resource.like_field:
                    if column_class == String:
                        _type = 'string'
                    elif column_class == Date:
                        _type = 'date'
                    else:
                        _type = 'integer'
                    self.parameter(name, 'query', _type)
        path = resource.uri
        if '<string:parent_id>' in path:
            path = self.path(path, resource.parent_id_field)
            self.parameter(resource.parent_id_field, 'path', 'string', require=True)

        self.response(get_schema_name)
        self.get_opt(f"获取{resource.name}的列表", tags=[resource.name])

        if '<string:parent_id>' in path:
            self.parameter(resource.parent_id_field, 'path', 'string', require=True)
        self.request_body(resource.PostSchema.__name__)
        self.response(resource.Schema.__name__)
        self.post_opt(f"创建{resource.name}", tags=[resource.name])

        if '<string:parent_id>' in path:
            self.parameter(resource.parent_id_field, 'path', 'string', require=True)
        self.request_body(IDSchema.__name__)
        self.response(description='删除成功')
        self.delete_opt(f"批量删除{resource.name}", tags=[resource.name])

        self.create(path=path, )

    def detail_docs(self, resource):

        path_parameter_name = f'{resource.Model.__name__}Id'
        path = self.path(resource.uri, path_parameter_name)
        self.parameter(path_parameter_name, 'path', 'string', require=True)
        self.response(resource.Schema.__name__)
        self.get_opt(f"获取单个{resource.name}", tags=[resource.name])

        self.parameter(path_parameter_name, 'path', 'string', require=True)
        self.request_body(resource.PutSchema.__name__)
        self.response(resource.Schema.__name__)
        self.put_opt(f"修改{resource.name}", tags=[resource.name])

        self.response(description='删除成功')
        self.parameter(path_parameter_name, 'path', 'string', require=True)
        self.delete_opt(f"删除单个{resource.name}", tags=[resource.name])

        self.create(path=path)

    # def common_docs(self, resources):
    #     for resource in resources:
    #         if issubclass(resource, ListResource):
    #             self.list_docs(resource)
    #         else:
    #             self.detail_docs(resource)
    #     return self.to_dict()
