import six, sqlalchemy as sa, datetime, uuid
from sqlalchemy.orm import object_mapper
from flask import g


class ModelIterator(six.Iterator):

    def __init__(self, model, columns):
        self.model = model
        self.i = columns

    def __iter__(self):
        return self

    # In Python 3, __next__() has replaced next().
    def __next__(self):
        n = six.next(self.i)
        return n, getattr(self.model, n)


class BaseModel(object):

    def __init__(self):
        self.__table__ = None

    def delete(self, session):
        with session.begin(subtransactions=True):
            session.delete(self)
            session.flush()

    def save(self, session):
        """Save this object."""
        with session.begin(subtransactions=True):
            session.add(self)
            session.flush()

    def update(self, values):
        """Make the model object behave like a dict."""
        for k, v in values.items():
            if hasattr(self, k):
                try:
                    setattr(self, k, v)
                except AttributeError:
                    continue

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):

        try:
            getattr(self, key)
        except AttributeError:
            return False
        else:
            return True

    def get(self, key, default=None):
        return getattr(self, key, default)

    @property
    def _extra_keys(self):
        """Specifies custom fields

        Subclasses can override this property to return a list
        of custom fields that should be included in their dict
        representation.

        For reference check tests/sa/sqlalchemy/test_models.py
        """
        return []

    def __iter__(self):
        columns = list(dict(object_mapper(self).columns).keys())
        columns.extend(self._extra_keys)

        return ModelIterator(self, iter(columns))

    def _as_dict(self):
        """Make the model object behave like a dict.

        Includes attributes from joins.
        """
        local = dict((key, value) for key, value in self)
        # print(local)
        joined = dict([(k, v) for k, v in six.iteritems(self.__dict__)
                       if not k[0] == '_'])
        local.update(joined)
        return local

    def iteritems(self):
        """Make the model object behave like a dict."""
        return six.iteritems(self._as_dict())

    def items(self):
        """Make the model object behave like a dict."""
        return self._as_dict().items()

    def keys(self):
        """Make the model object behave like a dict."""
        return list(self._as_dict().keys())

    def as_dict(self):
        return self._as_dict()


def get_group():
    if hasattr(g, 'user'):
        return g.user.get('group').get('id')


def get_group_name():
    if hasattr(g, 'user'):
        return g.user.get('group').get('name')


def get_user():
    if hasattr(g, 'user'):
        return g.user.get('id')


def get_tenant():
    if hasattr(g, 'user'):
        return g.user.get('tenant')


def get_user_name():
    if hasattr(g, 'user'):
        return g.user.get('name')


class TimestampMixin(object):
    create_time = sa.Column(sa.DateTime, default=datetime.datetime.now)
    modify_time = sa.Column(sa.DateTime, onupdate=datetime.datetime.now, default=datetime.datetime.now)


class DataPermissionMixin(object):
    user_id = sa.Column(sa.String(50), nullable=True, default=get_user)
    group_id = sa.Column(sa.String(50), default=get_group)
    tenant_id = sa.Column(sa.String(50), default=get_tenant)
    create_user = sa.Column(sa.String(50), default=get_user_name)
    create_group = sa.Column(sa.String(50), default=get_group_name)


class SoftDeleteMixin(object):
    is_delete = sa.Column(sa.Integer, default=0)


class IdMixin(object):
    id = sa.Column(sa.String(50), primary_key=True, unique=True, default=uuid.uuid4().hex)


class MainMixIn(IdMixin, TimestampMixin, SoftDeleteMixin):
    pass


class AllMixIn(MainMixIn, DataPermissionMixin):
    pass
