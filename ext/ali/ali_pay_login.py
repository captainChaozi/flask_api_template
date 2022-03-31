from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.request.AlipaySystemOauthTokenRequest import AlipaySystemOauthTokenRequest
from alipay.aop.api.response.AlipaySystemOauthTokenResponse import AlipaySystemOauthTokenResponse

# -*- coding: utf-8 -*-
'''
Created on 2017-12-20

@author: liuqun
'''
import base64

from alipay.aop.api.constant.CommonConstants import PYTHON_VERSION_3
from alipay.aop.api.exception.Exception import RequestException
from Crypto.Cipher import AES


BLOCK_SIZE = AES.block_size
pad = lambda s, length: s + (BLOCK_SIZE - length % BLOCK_SIZE) * chr(BLOCK_SIZE - length % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


def encrypt_content(content, encrypt_type, encrypt_key, charset):
    if "AES" == encrypt_type.upper():
        return aes_encrypt_content(content, encrypt_key, charset)
    raise RequestException("当前不支持该算法类型encrypt_type=" + encrypt_type)


def aes_encrypt_content(content, encrypt_key, charset):
    length = None
    if PYTHON_VERSION_3:
        length = len(bytes(content, encoding=charset))
    else:
        length = len(bytes(content))
    padded_content = pad(content, length)
    iv = '\0' * BLOCK_SIZE
    cryptor = AES.new(base64.b64decode(encrypt_key), AES.MODE_CBC, iv)
    encrypted_content = cryptor.encrypt(padded_content)
    encrypted_content = base64.b64encode(encrypted_content)
    if PYTHON_VERSION_3:
        encrypted_content = str(encrypted_content, encoding=charset)
    return encrypted_content


def decrypt_content(encrypted_content, encrypt_type, encrypt_key, charset):
    if "AES" == encrypt_type.upper():
        return aes_decrypt_content(encrypted_content, encrypt_key, charset)
    raise RequestException("当前不支持该算法类型encrypt_type=" + encrypt_type)


def aes_decrypt_content(encrypted_content, encrypt_key, charset):
    encrypted_content = base64.b64decode(encrypted_content)
    iv = ('\0' * BLOCK_SIZE).encode('utf-8')
    cryptor = AES.new(base64.b64decode(encrypt_key), AES.MODE_CBC, iv)
    content = unpad(cryptor.decrypt(encrypted_content))
    if PYTHON_VERSION_3:
        content = content.decode(charset)
    return content



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

        content = aes_decrypt_content(
            message, self.alipay_aes, charset)
        self.app.logger.info(content)
        return content
