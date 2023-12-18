import json
from pathlib import Path
from typing import Dict

from file_data_transfer_api.api.api_datamodel import \
    FileMetadata, FileDatabaseEntry
from file_data_transfer_api.utils.env_variables import DATABASE_PATH

def update_database_json(entry: FileDatabaseEntry):
    """Updates the database with a new or updated entry.

    Args:
        entry: a file entry to be added or updated in the database.
    """
    content = load_database_json()
    content.update(entry.to_database_format())
    dump_to_database_json(content=content)

def write_bytes_to_location(
    file_contents: bytes,
    path_to_save_location: Path,
):
    with open(path_to_save_location, "wb") as f:
        f.write(file_contents)

def remove_database_entry(file_id: str) -> FileMetadata:
    """Removes an entry from teh database.

    Args:
        file_id: unique file identifier of the file to be removed.

    Returns:
        Metadata stored against the file_id.
    """
    database_content = load_database_json()
    entry_metadata = FileMetadata(**database_content[file_id])
    del database_content[file_id]
    dump_to_database_json(content=database_content)
    return entry_metadata


def load_database_json() -> Dict[str, str]:
    """Returns json database as dictionary."""
    with open(DATABASE_PATH, "r") as local_file:
        content = json.load(local_file)
    return content


def dump_to_database_json(content: Dict[str, str]):
    """Updates database to content.

    Args:
        content: dictionary containing all database information.
    """
    with open(DATABASE_PATH, "w") as local_file:
        json.dump(content, local_file)


def get_metadata_from_file_id(file_id: str) -> FileMetadata:
    """Returns file metadata based on file_id."""
    database_content = load_database_json()
    return FileMetadata(**database_content[file_id])
