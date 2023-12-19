from abc import ABC, abstractmethod


class AbstractFileSystem(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def upload_content(
        self, content: bytes, filename: str,
    ):
        pass

    @abstractmethod
    def delete_file(self, file_id: str):
        pass
