# from marshmallow import fields, Schema
#
# from app.model import User
#
# from ext import BaseSchema, MetaBase, PostMetaBase
#
#
# class AliUserSchema(BaseSchema):
#     score = fields.Integer(description='西引力')
#     value = fields.Function(lambda obj: '{:,}'.format(obj.value), )
#     home_team = fields.Nested("TeamSchema")
#     card_team = fields.Nested('TeamSchema')
#     level = fields.String(description='等级')
#     next_level = fields.String(description="等级")
#     next_pre = fields.Integer(description='百分比')
#
#     class Meta(MetaBase):
#         model = User
#
#
# class AliUserPostSchema(Schema):
#     code = fields.String(required=True, description='支付宝登陆CODE')
#
#
# class AliUserPutSchema(AliUserSchema):
#     class Meta(PostMetaBase):
#         exclude = ("id", "create_time", "modify_time", "score", "alipay_id", "value")

