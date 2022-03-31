from app.ext_init import db
from ext import BaseMixIn


class User(db.Model, BaseMixIn):
    name = db.Column(db.String(100), doc="真实姓名")
    user_no = db.Column(db.String(50), doc='用户编码')
