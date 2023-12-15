from dataclasses import dataclass, asdict

from file_data_transfer_api.utils.env_variables import UPLOAD_PATH


@dataclass
class FileMetadata:
    filename: str

    def to_dict(self):
        return asdict(self)

    @property
    def filepath(self):
        return UPLOAD_PATH / self.filename

@dataclass
class FileDatabaseEntry:
    file_id: str
    metadata: FileMetadata

    def to_database_format(self):
        return {self.file_id: self.metadata.to_dict()}
