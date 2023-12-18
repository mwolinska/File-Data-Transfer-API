import os
import uuid

from fastapi import FastAPI, UploadFile
from starlette.responses import FileResponse

from file_data_transfer_api.api.api_datamodel import \
    FileMetadata, FileDatabaseEntry
from file_data_transfer_api.utils.env_variables import UPLOAD_PATH
from file_data_transfer_api.utils.file_saving_utils import \
    update_database_json, load_database_json, get_metadata_from_file_id, \
    remove_database_entry, write_bytes_to_location

app = FastAPI()


@app.post(path="/files/")
async def upload_file(file: UploadFile) -> FileDatabaseEntry:
    """Uploads file to the database.

    Args:
        file: file to be uploaded to database.

    Returns:
        Information stored in the database about this file including its
        uniqe id and its metadata.
    """
    contents = await file.read()

    write_bytes_to_location(
        file_contents=contents,
        path_to_save_location=UPLOAD_PATH / file.filename,
    )

    file_info = FileDatabaseEntry(
        file_id=str(uuid.uuid4()),
        metadata=FileMetadata(
                filename=file.filename,
                ),
        )

    update_database_json(entry=file_info)
    return file_info

@app.get(path="/files/{fileId}")
async def download_file(fileId: str) -> FileResponse:
    """Retrieves file based on a fileId allowing."""
    database_content = load_database_json()
    file_info = FileMetadata(**database_content[fileId])
    return FileResponse(
            file_info.filepath, filename=file_info.filename,
            headers={
                "filename": file_info.filename,
                "file_id": fileId,
            },
    )

@app.put(path="/files/{fileId}")
async def rename_file(fileId: str, newFilename: str) -> FileDatabaseEntry:
    """Renames a file in the database.

    Args:
        fileId: file id under which the file is stored.
        newFilename: new filename.

    Returns:
        The updated database entry.
    """
    entry_metadata = get_metadata_from_file_id(file_id=fileId)
    file_suffix = entry_metadata.filename.split(".")[-1]
    new_filename = newFilename + "." + file_suffix

    entry_metadata.filepath.rename(UPLOAD_PATH / new_filename)

    entry_metadata.filename = new_filename
    updated_entry = FileDatabaseEntry(
        file_id=fileId,
        metadata=entry_metadata
    )

    update_database_json(entry=updated_entry)
    return updated_entry


@app.delete(path="/files/{fileId}")
async def delete_file(fileId: str) -> FileDatabaseEntry:
    """Deletes file and removes entry from database.

    Args:
        fileId: file id under which the file is stored.

    Returns:
        Entry that was deleted from the database.
    """
    entry_metadata = remove_database_entry(file_id=fileId)
    os.remove(path=entry_metadata.filepath)
    return FileDatabaseEntry(
        file_id=fileId,
        metadata=entry_metadata,
    )
