from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.request.AlipaySystemOauthTokenRequest import AlipaySystemOauthTokenRequest
from alipay.aop.api.response.AlipaySystemOauthTokenResponse import AlipaySystemOauthTokenResponse
from alipay.aop.api.util import EncryptUtils


class AlipayOauth(object):

    def __init__(self, app=None):
        self.app = app
        self.app_id = None
        self.app_private_key = None
        self.alipay_public_key = None
        self.alipay_aes = None
        if app:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.app_id = app.config['ALIPAY_APP_ID']
        self.app_private_key = app.config['ALIPAY_PRIVATE_KEY']
        self.alipay_public_key = app.config['ALIPAY_PUBLIC_KEY']
        self.alipay_aes = app.config['ALIPAY_AES']

    def get_alipay_id(self, code):
        alipay_client_config = AlipayClientConfig()
        alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
        alipay_client_config.app_id = self.app_id
        alipay_client_config.app_private_key = self.app_private_key  # 应用私钥
        alipay_client_config.alipay_public_key = self.alipay_public_key  # 支付宝公钥
        client = DefaultAlipayClient(alipay_client_config, self.app.logger)

        request = AlipaySystemOauthTokenRequest()

        request.code = code  # auth_code小程序上传的
        request.grant_type = "authorization_code"

        # 执行API调用
        try:
            response_content = client.execute(request)
        except Exception as e:
            self.app.logger.error(e)
            response_content = None

        if response_content:
            # 解析响应结果
            response = AlipaySystemOauthTokenResponse()
            response.parse_response_content(response_content)

            if response.is_success():
                return response.user_id
            else:
                self.app.logger.error(
                    response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)
                return None

    def decrypt_phone(self, message):
        charset = 'utf-8'

        content = EncryptUtils.aes_decrypt_content(
            message, self.alipay_aes, charset)
        self.app.logger.info(content)
        return content
