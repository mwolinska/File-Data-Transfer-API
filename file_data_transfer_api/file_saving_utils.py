import json
from pathlib import Path
from typing import Dict

from file_data_transfer_api.api_datamodel import \
    FileMetadata, FileDatabaseEntry
from file_data_transfer_api.env_variables import DATABASE_PATH

def update_database_json(entry: FileDatabaseEntry):
    content = load_database_json()
    content.update(entry.to_database_format())
    dump_to_database_json(content=content)


def remove_database_entry(file_id: str) -> FileMetadata:
    database_content = load_database_json()
    entry_metadata = FileMetadata(**database_content[file_id])
    del database_content[file_id]
    dump_to_database_json(content=database_content)
    return entry_metadata


def write_file_to_location(
    file_contents: bytes,
    path_to_save_location: Path,
):
    with open(path_to_save_location, "wb") as f:
        f.write(file_contents)


def load_database_json():
    with open(DATABASE_PATH, "r") as local_file:
        content = json.load(local_file)
    return content


def dump_to_database_json(content: Dict[str, str]):
    with open(DATABASE_PATH, "w") as local_file:
        json.dump(content, local_file)


def get_metadata_from_file_id(file_id: str) -> FileMetadata:
    database_content = load_database_json()
    return FileMetadata(**database_content[file_id])
