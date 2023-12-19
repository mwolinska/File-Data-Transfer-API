from abc import ABC, abstractmethod
from pathlib import Path


class AbstractFileSystem(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def upload_content(
        self, content: bytes, filename: str,
    ):
        pass

    @abstractmethod
    def change_filename(self, path_to_file: Path, new_filename: str):
        pass

    @abstractmethod
    def delete_file(self, file_id: str):
        pass
