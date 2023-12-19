import uuid

from fastapi import FastAPI, UploadFile
from starlette.responses import FileResponse

from database_client.database_manager import DatabaseManager
from file_client.file_manager import FileManager
from database_client.datamodel.database_entry import \
    FileMetadata, FileDatabaseEntry

app = FastAPI()

@app.post(path="/files/")
async def upload_file(file: UploadFile) -> FileDatabaseEntry:
    """Uploads file to the database.

    Args:
        file: file to be uploaded to database.

    Returns:
        Information stored in the database about this file including its
        unique id and its metadata.
    """
    contents = await file.read()

    file_info = FileDatabaseEntry(
        file_id=str(uuid.uuid4()),
        metadata=FileMetadata(
                filename=file.filename,
                ),
        )

    FileManager.upload_file(file_content=contents, file_id=file_info.file_id)
    DatabaseManager.add_entry(entry=file_info)
    return file_info

@app.get(path="/files/{fileId}")
async def download_file(fileId: str) -> FileResponse:
    """Retrieves file based on a fileId allowing."""
    file_info = DatabaseManager.retrieve_entry(item_id=fileId)
    return FileResponse(
            FileManager.path_to_file(file_id=fileId),
            headers={
                "filename": file_info.metadata.filename,
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
    database_entry = DatabaseManager.retrieve_entry(item_id=fileId)
    file_suffix = database_entry.metadata.filename.split(".")[-1]
    new_filename = newFilename + "." + file_suffix
    updated_entry = FileDatabaseEntry(
        file_id=fileId,
        metadata=FileMetadata(
            filename=new_filename,
        )
    )
    DatabaseManager.update_entry(database_entry=updated_entry)
    return updated_entry


@app.delete(path="/files/{fileId}")
async def delete_file(fileId: str) -> FileDatabaseEntry:
    """Deletes file and removes entry from database.

    Args:
        fileId: file id under which the file is stored.

    Returns:
        Entry that was deleted from the database.
    """
    entry = DatabaseManager.delete_entry(item_id=fileId)
    FileManager.delete_file(
        file_id=fileId,
    )
    return entry
