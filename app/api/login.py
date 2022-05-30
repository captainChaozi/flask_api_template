from app.ext_init import docs
from ext import BaseResource, res_convert


class LoginApi(BaseResource):
    name = '登录'
    uri = '/login'
    docs = docs
    tag_group = 'Oauth'

    def post(self):
        if self.data.get('name') == 'admin' and self.data.get('password') == 'admin':
            return res_convert(
                {"token": "dads;jasldj;asd", "name": "admin"}
            )


class TestApi(BaseResource):
    uri = '/test'

    def post(self):
        return {
            "status": 401,
            "msg": "请重新登录",
            "data": {
            }
        }


class ErrorAPI(BaseResource):
    uri = '/error'

    def post(self):
        return {
            "status": 400,
            "msg": "这到底是咋了",
            "data": {
            }
        }
