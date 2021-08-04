import atexit
from datetime import datetime
from typing import Final

from api.services.file import YandexDisk
from api.utils.functions import file_line_count

__all__ = ['LogsDrainer']


class LogsDrainer:
    def __init__(
        self, path_to_logs_file: str, max_line_count: int = 1000,
        directory_to_upload: str = '/logs'
    ):
        """
        :param path_to_logs_file: absolute path (from BASE_DIR) to the logs file
            (including the filename)
        :param max_line_count: the number of lines at which the file is loaded to the
            file base and cleared
        :param directory_to_upload: directory on the file base for uploading logs
            (the file name is generated automatically as the current time)
        """
        self._path_to_logs_file: Final[str] = path_to_logs_file
        self._max_line_count: Final[int] = max_line_count
        self._directory_to_upload: Final[str] = directory_to_upload
        
        self.__file_store = YandexDisk()
        
        atexit.register(self._upload_logs_and_clear)
    
    def check(self) -> None:
        with open(self._path_to_logs_file, 'r') as logs_file:
            logs_line_count = file_line_count(logs_file)
        
        if logs_line_count >= self._max_line_count:
            self._upload_logs_and_clear()
    
    @property
    def _path_to_upload(self) -> str:
        return f'{self._directory_to_upload}/{self._filename}.log'
    
    @property
    def _filename(self) -> str:
        return datetime.utcnow().strftime("%d-%m-%Y_%H-%M-%S")
    
    def _upload_logs_and_clear(self) -> None:
        with open(self._path_to_logs_file, 'rb') as logs_file:
            self.__file_store.upload(logs_file, self._path_to_upload)
        open(self._path_to_logs_file, 'w').close()  # clear logs file
