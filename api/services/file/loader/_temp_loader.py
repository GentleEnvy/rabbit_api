from __future__ import annotations

from datetime import datetime
import os
from pathlib import Path
import shutil
from typing import Final

from docxtpl import DocxTemplate

__all__ = ['TempFileLoader']


def _generate_temp_filename() -> str:
    return f'temp_{int(datetime.utcnow().timestamp() * 10000)}'


class TempFileLoader:
    PATH_TO_TEMP: Final[Path] = Path(__file__).parent / '_temp'
    
    shutil.rmtree(PATH_TO_TEMP, ignore_errors=True)
    os.makedirs(PATH_TO_TEMP, exist_ok=True)
    
    @classmethod
    def from_document(cls, document: DocxTemplate) -> TempFileLoader:
        loader = TempFileLoader()
        document.save(loader.path)
        return loader
    
    def __init__(self, filename: str = None):
        self.filename: Final[str] = filename or _generate_temp_filename()
        open(self.path, 'a')
    
    @property
    def path(self) -> Path:
        return self.PATH_TO_TEMP / self.filename
    
    def open(self, mode: str = 'rb'):
        return open(self.path, mode)
    
    def close(self):
        self.path.unlink(missing_ok=True)
    
    def __del__(self):
        self.close()
