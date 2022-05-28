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
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), nullable=False)


class User(db.Model, BaseMixIn):
    """
    user 是一个单租户的表,然后一个公司做数据隔离,然后可以根据group做数据隔离
    """
    tenant_id = db.Column(db.String(50), db.ForeignKey('tenant.id'), nullable=False)
    tenant = db.relationship('Tenant', backref=db.backref('users', lazy='dynamic'), lazy='joined')
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255))
    name = db.Column(db.String(50))
    phone = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    position = db.Column(db.String(50))
    token = db.Column(db.String(256))
    group_id = db.Column(db.String(50), db.ForeignKey('group.id', ondelete='SET NUll'))
    group = db.relationship('Group', lazy='joined')
    data_permission = db.relationship('DataPermission', lazy='joined', cascade='all,delete-orphan')
    roles = db.relationship('Role', secondary=user_role_table, lazy='joined')
    is_admin = db.Column(db.Integer, default=0)


class Role(db.Model, BaseMixIn):
    name = db.Column(db.String(50))
    permissions = db.relationship('Permission', secondary=role_permission_table, backref=db.backref('roles'))
    tenant_id = db.Column(db.String(50), db.ForeignKey('tenant.id'))
    tenant = db.relationship('Tenant', backref=db.backref('roles', lazy='dynamic'))


class Permission(db.Model, BaseMixIn):
    name = db.Column(db.String(50))
    permission_group = db.Column(db.String(50))
    key = db.Column(db.String(50))


class Group(db.Model, BaseMixIn):
    name = db.Column(db.String(50))
    code = db.Column(db.String(50))
    parent_id = db.Column(db.ForeignKey('group.id'))
    children = db.relationship('Group', remote_side=[parent_id])
    tenant_id = db.Column(db.String(50), db.ForeignKey('tenant.id'))
    data_permission = db.relationship('DataPermission', secondary=group_permission_table)
    is_delete = db.Column(db.Integer, default=0)


class DataPermission(db.Model, BaseMixIn):
    """
    数据权限的表
    self 自己组 这是历史遗留问题,为了兼容老的oauth
    all 全部组别,这个具有极高的权限
    group 指定组别
    my 自己的数据,只能查询自己的,filter的时候user_id
    """
    __tablename__ = 'data_permission'
    user_id = db.Column(db.String(50), db.ForeignKey('user.id', ondelete='CASCADE'))
    type = db.Column(db.Enum('self', 'all', 'group', name='type'), nullable=False)
    groups = db.relationship("Group", secondary=group_permission_table)
