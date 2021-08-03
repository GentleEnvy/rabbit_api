from typing import Final

from django.conf import settings
from yadisk import YaDisk
from yadisk.exceptions import PathExistsError

__all__ = ['YandexDisk']


class YandexDisk:
    def __init__(self, token: str = None):
        self.ya_disk: Final[YaDisk] = YaDisk(
            token=token or settings.YANDEX_DISK_TOKEN
        )
        if not self.ya_disk.check_token():
            raise ValueError('Yandex disk token is invalid')
    
    def upload(self, file, path):
        try:
            self.ya_disk.upload(file, path)
        except PathExistsError:
            raise FileExistsError
