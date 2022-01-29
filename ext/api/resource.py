from flask import g, request, current_app
from sqlalchemy import or_
from flask_restful import Resource
from ext.api.base_schema import BaseSchema, ExportSchema
from .api_utils import abort, param_query, paginator, soft_delete, real_delete


class BaseService(object):
    """
    核心service 类使用必须是在一个appcontext 和 request context 里面
    每个service 对应一个CONFIG CONFIG 类控制接口的显示状态
    """

    def __init__(self):
        self.db_session = g.db_session
        self.query = None
        # self.config = self.Config(self.config_type)
        self.create_query()

    def create_query(self):
        self.query = None

    def before_post(self, data):
        """

        :param data: schema序列化之后的数据,建议在schema层进行数据转化,在这一层进行数据校验
        :return: data
        """
        return data

    def after_post(self, resource, data):
        """

        :param resource: 创建出来的资源
        :param data: 创建资源需要的数据
        :return: None
        """
        return resource

    def before_review(self, resource, data):
        """

        :param resource: 要审核的资源
        :param data: 审核的驱动状态
        :return: 审核的资源
        """
        return resource

    def after_review(self, resource, data):
        """

        :param resource: 要审核的资源
        :param data: 审核的驱动状态
        :return: 审核的资源
        """
        return resource

    def before_delete(self, data):
        """

        :param data: 这是删除之前的数据
        :return:
        """
        return data

    def after_delete(self, resources, data):
        """

        :param resources: 删除的资源的list
        :param data:
        :return:
        """
        return

    def before_put(self, data):
        """

        :param data: schema 序列化之后的数据
        :return:
        """
        return data

    def after_put(self, resource, data):
        """

        :param resource: 修改的资源
        :param data: 数据
        :return:
        """
        return resource


class BaseResource(Resource):
    name = ''  # 资源名称
    uri = '/'  # 注册URI
    parent_name = ''

    def __init__(self, data=None, param=None):
        self.db_session = g.db_session
        self.logger = current_app.logger
        if param:
            self.param = param
        else:
            self.param = dict()
            if request.args:
                self.param = request.args
        if data:
            self.data = data
        else:
            self.data = dict()
            if request.method != 'GET' and request.get_json():
                self.data = request.json()

        self.logger.debug(request.url + " args:" + str(self.param))
        self.logger.debug(request.url + " body:" + str(self.data))

        super().__init__()


class ListResource(BaseResource):
    name = ''  # 资源名称
    uri = '/'  # 注册URI
    parent_name = ''
    Schema = BaseSchema  # 利用这个schema 来配置
    PostSchema = BaseSchema
    ExcelSchema = ExportSchema
    Model = None  # 操作那些资源
    Service = BaseService
    parent_id_field = None  # 父ID字段名
    like_field = ()  # 单字段模糊搜索参数
    search_field = ()  # search 参数搜索
    between_field = ()  # 之间查询参数
    in_field = ()  # in 参数搜索
    soft_delete = True  # 假删除
    order_by_field = ()  # 噢爱须字段
    not_repeat_field = dict()  # {"field":"字段意义",} 不允许重复字段

    def __init__(self, data=None, param=None):
        super().__init__(data=data, param=param)
        self.query = self.db_session.query(self.Model)
        self.service = self.Service()

    def create_order_by(self):
        """
        sql order_by
        @update: sqlalchemy.exc.CompileError: MSSQL requires an order_by
        when using an OFFSET or a non-simple LIMIT clause
        @date: 2020/04/27
        @return:
        """
        if self.order_by_field != ():
            self.query = self.query.order_by(*self.order_by_field)
        else:
            if hasattr(self.Model, 'modify_time'):
                self.query = self.query.order_by(self.Model.modify_time.desc())

    def create_query(self):
        if self.param:
            query_obj = param_query([self.Model], param=self.param, like_fields=self.like_field,
                                    between_field=self.between_field, in_field=self.in_field)
            self.query = self.query.filter(*query_obj)
        if self.search_field and 'search' in self.param:
            search_str = []
            if self.param.get('search'):
                for i in self.search_field:
                    if '.' in i:
                        json_filed = i.split('.')[0]
                        attr = i.split('.')[1]
                        search_str.append(
                            getattr(self.Model, json_filed)[attr].astext.like("%{}%".format(self.param.get('search'))))
                    else:

                        search_str.append(getattr(self.Model, i).like("%{}%".format(self.param.get('search'))))
                self.query = self.query.filter(or_(*search_str))

        if hasattr(self.Model, 'is_delete'):
            self.query = self.query.filter(self.Model.is_delete == 0)

    def get(self, parent_id=None):

        # 可以定制化的写query对象
        if self.service.query:
            self.query = self.service.query
        self.create_order_by()
        self.create_query()
        if parent_id:
            self.query = self.query.filter(getattr(self.Model, self.parent_id_field) == parent_id)

        schema = self.Schema(many=True)
        if 'excel' in self.param:
            schema = self.ExcelSchema(many=True)
            schema.context = {'file_name': str(self.service) + '.xls'}
            return schema.dump(self.query)
        return paginator(self.query, schema)

    def post(self, parent_id=None):
        schema = self.PostSchema()
        data = schema.load(self.data)
        for field in self.not_repeat_field:
            repeat = self.query.filter(getattr(self.Model, field) == data.get(field),
                                       self.Model.is_delete == 0).first()
            if repeat:
                abort(400, message=self.not_repeat_field[field] + "已经存在,请更换")
        with self.db_session.begin(subtransactions=True):
            data['parent_id'] = parent_id
            data = self.service.before_post(data)
            resource = self.Model()
            resource.update(data)
            if parent_id:
                setattr(resource, self.parent_id_field, parent_id)
            resource.save(self.db_session)
            resource = self.service.after_post(resource, data)
            schema = self.Schema()
            return schema.dump(resource)

    def delete(self, parent_id=None):
        with self.db_session.begin(subtransactions=True):
            ids = self.data['ids']
            for i in ids:
                self.service.before_delete(self.data)
                if self.soft_delete:
                    resources = soft_delete(self.Model, i)
                else:
                    resources = real_delete(self.Model, i)
                self.service.after_delete(resources, self.data)


class DetailResource(BaseResource):
    Model = None
    Schema = BaseSchema
    PutSchema = BaseSchema
    Service = BaseService
    not_repeat_field = dict()
    parent_id_field = None
    soft_delete = True

    def __init__(self, data=None, param=None):
        super().__init__(data=data, param=param)
        self.service = self.Service()

    def get(self, resource_id):
        resource = self.db_session.query(self.Model).filter(self.Model.id == resource_id).first()
        schema = self.Schema()
        return schema.dump(resource)

    def put(self, resource_id):
        resource = self.db_session.query(self.Model).filter(self.Model.id == resource_id).first()
        schema = self.PutSchema()
        data = schema.load(self.data)
        for field in self.not_repeat_field:
            repeat = self.db_session.query(self.Model).filter(getattr(self.Model, field) == data.get(field),
                                                              self.Model.is_delete == 0).first()
            if repeat and resource.id != repeat.id:
                abort(400, message=self.not_repeat_field[field] + "已经存在,请更换")
        with self.db_session.begin(subtransactions=True):
            if self.parent_id_field:
                data['parent_id'] = getattr(resource, self.parent_id_field)
            data = self.service.before_put(data)
            resource.update(data)
            resource.save(self.db_session)
            resource = self.service.after_put(resource, data)
            schema = self.Schema()
            return schema.dump(resource)
