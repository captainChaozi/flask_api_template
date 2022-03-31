import datetime
import sys

import oss2
import requests

from utils.unique_tools import generate_unique


class AliOSS(object):

    def __init__(self, app=None,
                 access_key_id=None,
                 access_key_secret=None,
                 endpoint=None,
                 bucket_name=None,
                 oss_domain=None):
        self.app = app
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        self.oss_domain = oss_domain
        if app:
            self.init_app(app)

    def init_app(self, app=None):
        self.app = app
        self.validate_config()

    def validate_config(self):
        config = ('OSS_KEY_ID', 'OSS_KEY_SECRET', 'OSS_BUCKET', 'OSS_ENDPOINT')
        for i in config:
            if i not in self.app.config:
                print('{}没有设置'.format(i))
                sys.exit(1)
        self.access_key_id = self.app.config['OSS_KEY_ID']
        self.access_key_secret = self.app.config['OSS_KEY_SECRET']
        self.endpoint = self.app.config['OSS_ENDPOINT']
        self.bucket_name = self.app.config['OSS_BUCKET']
        self.oss_domain = self.app.config.get('OSS_DOMAIN')

    @property
    def bucket(self):
        return oss2.Bucket(oss2.Auth(self.access_key_id, self.access_key_secret),
                           self.endpoint, self.bucket_name)

    # 下载一个文件对象
    def down_file_obj(self, file_name):
        try:
            file = self.bucket.get_object(file_name)
        except oss2.exceptions.NoSuchKey as e:
            self.app.logger.error('已经被删除了：request_id={0}'.format(e.request_id))
            return False
        else:
            return file

    # 针对excel文件的需求只是上传下载一下
    def download(self, file_name, file_save_name):
        try:
            self.bucket.get_object_to_file(file_name, file_save_name)
        except oss2.exceptions.NoSuchKey as e:
            self.app.logger.error('已经被删除了：request_id={0}'.format(e.request_id))
            return False
        else:
            return True

    # 上传字符串
    def up_str(self, file_name, file_str):
        self.bucket.put_object(file_name, file_str)
        return True

    # 上传文件对象
    def up_file_obj(self, file_name, file):
        self.bucket.put_object(file_name, file)
        return True

    def upload(self, file_name, file):
        with open(oss2.to_unicode(file), 'rb') as f:
            self.bucket.put_object(file_name, f)
        return True

    def delete(self, file_name):
        self.bucket.delete_object(file_name)
        return True

    @property
    def url_prefix(self):
        if self.oss_domain:
            return self.oss_domain
        return 'http://' + self.bucket_name + '.' + self.endpoint + '/'

    @staticmethod
    def file_name(old, code=None):
        h = old.split('.')[-1]
        h = 'PNG'
        file_name = generate_unique(10)
        today = str(datetime.date.today())
        if code:
            return code + '/' + file_name + '.' + h
        return 'static/' + today + '/' + file_name + '.' + h

    def copy_file(self, old, new, bucket=None):
        if not bucket:
            bucket = self.bucket_name
        self.bucket.copy_object(bucket, old, new)
        return self.url_prefix + new

    def pull_file(self, url):
        res = requests.get(url)
        file_name = self.file_name(url)
        self.up_str(file_name, res.content)
        return self.url_prefix + file_name
