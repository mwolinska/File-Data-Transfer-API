from dataclasses import dataclass, asdict
from typing import Dict


@dataclass
class FileMetadata:
    """Captures metadata about a file to be stored in database.

    Args:
        filename: name of file to be saved.
    """
    filename: str

@dataclass
class FileDatabaseEntry:
    """Stores all information required to add a new file entry to the database.

    Args:
        file_id: unique file identifier.
        metadata: file metadata to be stored.
    """
    file_id: str
    metadata: FileMetadata

    def to_database_format(self) -> Dict[str, Dict[str, str]]:
        """Converts dataclass to dictionary to allow addition to database."""
        return {self.file_id: asdict(self.metadata)}
