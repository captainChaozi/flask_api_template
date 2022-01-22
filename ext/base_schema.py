import os
import uuid
from urllib.parse import quote

from flask import send_file, make_response
from marshmallow import fields, post_dump
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from pandas import DataFrame

from config import basedir


class MainSchema(SQLAlchemyAutoSchema):
    id = fields.String()
    create_time = fields.DateTime()
    modify_time = fields.DateTime()
    extend = fields.Raw()


class MetaBase:
    include_fk = True
    dateformat = '%Y-%m-%d'
    datetimeformat = '%Y-%m-%d %H:%M:%S'


class AllSchema(MainSchema):
    user_id = fields.String(allow_none=True)
    group_id = fields.String(allow_none=True)
    tenant_id = fields.String(allow_none=True)
    create_user = fields.String(allow_none=True)
    create_group = fields.String(allow_none=True)


class ExportSchema(MainSchema):

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
