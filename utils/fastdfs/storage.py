from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.conf import settings


class FdfsStorage(Storage):
    """
        自定义储存类
        利用fastdfs_client-python模块,实现Django通过fastdfs存储文件.
    """

    def _open(self, name, mode='rb'):
        pass

    def _save(self, name, content, max_length=None):
        client = Fdfs_client(settings.FDFS_CLIENT_CONF)  # 创建链接,指定配置文件.
        res = client.upload_by_buffer(content.read())  # 上传文件
        if res.get('Status') != 'Upload successed.':
            raise Exception('上传文件失败')
        remote_file_id = res.get('Remote file_id')  # 获取返回的文件id
        return remote_file_id

    def exists(self, name):
        return False  # Django不储存文件名,不存在文件名重复的情况.

    def url(self, name):
        name = settings.FDFS_STORAGE_URL + name
        return name
