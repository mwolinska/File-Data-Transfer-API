from pathlib import Path

from file_client.env_variables import UPLOAD_PATH
from file_client.file_system.local_file_system import LocalFileSystem


class FileManager:
    @staticmethod
    def _select_file_system(upload_path: Path):
        uri = Path(upload_path).as_uri()
        if "file://" in uri:
            return LocalFileSystem()
        # elif "" in uri:
        #     return S3FileSystem
        else:
            raise NotImplementedError(
                "This upload_path does not correspond to a known file system."
            )

    @classmethod
    def upload_file(cls, file_content: bytes, file_id: str):
        file_system = cls._select_file_system(
            upload_path=cls.path_to_file(file_id),
        )
        return file_system.upload_content(
            content=file_content,
            filename=file_id,
        )

    @classmethod
    def delete_file(cls, file_id: str):
        file_system = cls._select_file_system(
            upload_path=cls.path_to_file(file_id),
        )
        return file_system.delete_file(
            file_id=file_id,
        )

    @staticmethod
    def path_to_file(file_id: str):
        return (UPLOAD_PATH / file_id).absolute()
