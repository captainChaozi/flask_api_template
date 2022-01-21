from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


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
