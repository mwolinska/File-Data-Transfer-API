import os
from pathlib import Path

from file_client.env_variables import UPLOAD_PATH
from file_client.file_system.abstract_file_system import AbstractFileSystem


class LocalFileSystem(AbstractFileSystem):
    def upload_content(self, content: bytes, filename: str):
        """Saves content at UPLOAD_PATH location."""
        with open(UPLOAD_PATH / filename, "wb") as f:
            f.write(content)

    def delete_file(self, file_id: str):
        os.remove(path=UPLOAD_PATH / file_id)
