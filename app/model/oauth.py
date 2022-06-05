from sqlalchemy.dialects.postgresql import JSONB

from app.ext_init import db
from ext import BaseMixIn

group_permission_table = db.Table('group_permission',
                                  db.Column('group_id', db.String(50), db.ForeignKey('group.id'),
                                            primary_key=True),
                                  db.Column('data_permission_id', db.String(50),
                                            db.ForeignKey('data_permission.id'),
                                            primary_key=True)
                                  )

user_role_table = db.Table('user_role',
                           db.Column('user_id', db.String(50), db.ForeignKey('user.id'),
                                     primary_key=True),
                           db.Column('role_id', db.String(50), db.ForeignKey('role.id'), primary_key=True)
                           )

role_permission_table = db.Table('role_permission',
                                 db.Column('role_id', db.String(50), db.ForeignKey('role.id'), primary_key=True),
                                 db.Column('permission', db.String(50), db.ForeignKey('permission.id'),
                                           primary_key=True)
                                 )


class Tenant(db.Model, BaseMixIn):
    name = db.Column(db.String(100), nullable=False, doc='租户名称')
    code = db.Column(db.String(50), nullable=False, doc='租户编码')


class User(db.Model, BaseMixIn):
    tenant_id = db.Column(db.String(50), db.ForeignKey('tenant.id'), nullable=False, doc='租户ID')
    tenant = db.relationship('Tenant', backref=db.backref('users', lazy='dynamic'), lazy='joined')
    username = db.Column(db.String(100), nullable=False, doc='用户名/登录')
    password = db.Column(db.String(255))  # 不要序列化
    nickname = db.Column(db.String(50), doc='昵称')
    phone = db.Column(db.String(50), doc='手机号')
    email = db.Column(db.String(50), doc='邮箱')
    position = db.Column(db.String(50), doc='岗位')
    group_id = db.Column(db.String(50), db.ForeignKey('group.id', ondelete='SET NUll'), doc='部门ID')
    group = db.relationship('Group', lazy='joined')
    data_permission = db.relationship('DataPermission', cascade='all,delete-orphan')
    roles = db.relationship('Role', secondary=user_role_table)
    is_admin = db.Column(db.Integer, default=0, doc='是否超级管理员')


class Role(db.Model, BaseMixIn):
    name = db.Column(db.String(50), doc='角色名称')
    permissions = db.relationship('Permission', secondary=role_permission_table, backref=db.backref('roles'))
    tenant_id = db.Column(db.String(50), db.ForeignKey('tenant.id'), doc='租户ID')
    tenant = db.relationship('Tenant', backref=db.backref('roles', lazy='dynamic'))


class PermissionGroup(db.Model, BaseMixIn):
    name = db.Column(db.String(50), doc='菜单名称')


class Permission(db.Model, BaseMixIn):
    name = db.Column(db.String(50), doc='权限项/次级菜单')
    permission_group_id = db.Column(db.String(50), db.ForeignKey('permission_group.id'), doc='权限组ID')
    permission_group = db.relationship('PermissionGroup', backref=db.backref('permission_groups', lazy='dynamic'))
    key = db.Column(db.String(50), doc='key')
    describe = db.Column(db.String(1000), doc='权限描述')
    page = db.Column(JSONB, doc='页面代码')


class Group(db.Model, BaseMixIn):
    name = db.Column(db.String(50), doc='部门名称')
    parent_id = db.Column(db.String(50), db.ForeignKey('group.id'), doc='父部门ID')
    children = db.relationship('Group', remote_side=[parent_id])
    tenant_id = db.Column(db.String(50), db.ForeignKey('tenant.id'), doc='租户ID')
    data_permission = db.relationship('DataPermission', secondary=group_permission_table)


class DataPermission(db.Model, BaseMixIn):
    user_id = db.Column(db.String(50), db.ForeignKey('user.id', ondelete='CASCADE'), doc='用户ID')
    type = db.Column(db.Enum('self', 'all', 'group', name='type'), nullable=False, doc='权限类型')
    groups = db.relationship("Group", secondary=group_permission_table)
