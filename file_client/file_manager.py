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
    def upload_file(cls, file_content: bytes, filename: str):
        file_system = cls._select_file_system(
            upload_path=Path(UPLOAD_PATH / filename).absolute())
        return file_system.upload_content(
            content=file_content,
            filename=filename,
        )

    @classmethod
    def update_filename(cls, old_name: Path, new_name: str):
        # TODO: change to work with ids rather than paths
        file_system = cls._select_file_system(
            upload_path=UPLOAD_PATH / old_name,
        )
        return file_system.change_filename(
            path_to_file=UPLOAD_PATH / old_name,
            new_filename=new_name,
        )

    @classmethod
    def delete_file(cls, file_id: str, temp_path: Path):
        file_system = cls._select_file_system(
            upload_path=temp_path,
        )
        return file_system.delete_file(
            file_id=file_id,
            temp_path=temp_path,
        )

    @staticmethod
    def path_to_file(filename: str):
        return UPLOAD_PATH / filename
