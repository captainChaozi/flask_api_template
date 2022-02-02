import os
import uuid
from urllib.parse import quote
from marshmallow import Schema
from flask import send_file, make_response
from marshmallow import fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from pandas import DataFrame

from config import basedir


class BaseSchema(SQLAlchemyAutoSchema):
    id = fields.String(dump_only=True)
    create_time = fields.DateTime(dump_only=True)
    modify_time = fields.DateTime(dump_only=True)
    extend = fields.Raw()


class IDSchema(Schema):
    ids = fields.List(cls_or_instance=fields.String)


class MetaBase:
    include_fk = True
    dateformat = '%Y-%m-%d'
    datetimeformat = '%Y-%m-%d %H:%M:%S'
    exclude = ('is_delete',)
    ordered = True


class PostMetaBase(MetaBase):
    exclude = ('id', 'create_time', 'modify_time', 'is_delete')


class AllSchema(BaseSchema):
    user_id = fields.String(allow_none=True)
    group_id = fields.String(allow_none=True)
    tenant_id = fields.String(allow_none=True)
    create_user = fields.String(allow_none=True)
    create_group = fields.String(allow_none=True)


class PagingSchema(Schema):
    page = fields.Integer()
    per_page = fields.Integer()
    total_number = fields.Integer()


class ExportSchema(BaseSchema):

    @post_dump(pass_many=True)
    def data_excel(self, data):
        data_frame = DataFrame.from_records(data=data)
        file_name = uuid.uuid4().hex + '.xls'
        file_path = os.path.join(basedir, file_name)
        data_frame.to_excel(excel_writer=file_path, index=False)
        response = make_response(send_file(file_path))
        basename = os.path.basename(self.context['file_name'])
        response.headers["Content-Disposition"] = \
            "attachment;" \
            "filename*=UTF-8''{utf_filename}".format(
                utf_filename=quote(basename.encode('utf-8'))
            )
        os.remove(file_path)

        return response
