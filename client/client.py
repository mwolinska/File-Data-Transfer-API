from io import BytesIO
from pathlib import Path
from typing import Union, Optional

import numpy as np
import requests
from PIL import Image

from database_client.datamodel.database_entry import FileDatabaseEntry, \
    FileMetadata


class Client:
    """Client-side functionality to facilitate access from client."""
    def __init__(self):
        self.url = "http://127.0.0.1:8000"

    def upload_file(self, path_to_file: Path) -> FileDatabaseEntry:
        """Uploads file and adds corresponding entry to database."""
        file_to_upload = {'file': open(path_to_file, 'rb')}
        response = requests.post(
            url=f"{self.url}/files",
            files=file_to_upload,
        )
        if response.ok:
            response = response.json()
            return FileDatabaseEntry(
                file_id=response["file_id"],
                metadata=FileMetadata(**response["metadata"])
            )
        else:
            raise ValueError(
                f"API could not be accessed. "
                f"Response error code {response.status_code}",
            )

    def access_file(
            self, file_id: str, path_to_save: Optional[Path] = None,
    ) -> Union[np.ndarray, str]:
        """Access file s

        Args:
            file_id: file id under which the file is stored.
            path_to_save: if passed, the location where the file will be saved.

        Returns:
            Decoded contents of the file as an array if the file is an image
            or as a string otherwise.
        """
        response = requests.get(f"{self.url}/files/{file_id}")
        if path_to_save is not None:
            with open(path_to_save / response.headers["filename"], "wb") \
                    as file:
                file.write(response.content)

        if "image" in response.headers["content-type"]:
            return np.array(Image.open(BytesIO(response.content)))
        else:
            try:
                return response.content.decode(encoding=response.encoding)
            except TypeError:
                raise NotImplementedError(
                    "This file type is not handled natively in this package."
                    "Run this function with path_to_save != None and "
                    "load the file manually."
                )

    def delete_file(self, file_id: str) -> FileDatabaseEntry:
        """Deletes file and corresponding entry in database."""
        response = requests.delete(url=f"{self.url}/files/{file_id}")
        if response.ok:
            response = response.json()
            return FileDatabaseEntry(
                file_id=response["file_id"],
                metadata=FileMetadata(**response["metadata"])
            )
        else:
            raise ValueError

    def update_filename(
            self, file_id: str, new_filename: str,
    ) -> FileDatabaseEntry:
        response = requests.put(
            url=f"{self.url}/files/{file_id}?newFilename={new_filename}",
        )

        if response.ok:
            response = response.json()
            return FileDatabaseEntry(
                file_id=response["file_id"],
                metadata=FileMetadata(**response["metadata"]),
            )
        else:
            raise ValueError(
                f"API could not be accessed. "
                f"Response error code {response.status_code}",
            )
