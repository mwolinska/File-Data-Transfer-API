import os
import uuid

import uvicorn
from fastapi import FastAPI, UploadFile
from starlette.responses import FileResponse

from file_data_transfer_api.api_datamodel import \
    FileMetadata, FileDatabaseEntry
from file_data_transfer_api.env_variables import UPLOAD_PATH
from file_data_transfer_api.file_saving_utils import update_database_json, \
    write_file_to_location, load_database_json, get_metadata_from_file_id, \
    remove_database_entry

app = FastAPI()


@app.post(path="/files/")
async def upload_file(file: UploadFile) -> FileDatabaseEntry:
    contents = await file.read()

    write_file_to_location(
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

@app.get(path="/files/{file_id}")
async def download_file(file_id: str) -> FileResponse:
    database_content = load_database_json()
    file_info = FileMetadata(**database_content[file_id])
    return FileResponse(file_info.filepath, filename=file_info.filename)

@app.put(path="/files/{file_id}")
async def rename_file(file_id: str,
                      new_filename: str,
                      ) -> FileDatabaseEntry:
    entry_metadata = get_metadata_from_file_id(file_id=file_id)
    file_suffix = entry_metadata.filename.split(".")[-1]
    new_filename = new_filename + "." + file_suffix

    entry_metadata.filepath.rename(UPLOAD_PATH / new_filename)

    entry_metadata.filename = new_filename
    updated_entry = FileDatabaseEntry(
        file_id=file_id,
        metadata=entry_metadata
    )

    update_database_json(entry=updated_entry)
    return updated_entry


@app.delete(path="/files/{file_id}")
async def delete_file(file_id: str) -> FileDatabaseEntry:
    entry_metadata = remove_database_entry(file_id=file_id)
    os.remove(path=entry_metadata.filepath)
    return FileDatabaseEntry(
        file_id=file_id,
        metadata=entry_metadata,
    )

if __name__ == '__main__':
    uvicorn.run(
        "playground:app",
        host="127.0.0.1",
        port=8000,
        reload_dirs="file_data_transfer_api",
        reload=True
    )
