from pathlib import Path

import requests

from file_data_transfer_api.api.api_datamodel import FileDatabaseEntry


class Client:
    """Client-side functionality to facilitate access from client."""
    def __init__(self):
        self.url = "http://127.0.0.1:8000"

    def upload_file(self, path_to_file: Path) -> FileDatabaseEntry:
        """Uploads file and adds corresponding entry to databse."""
        file_to_upload = {'file': open(path_to_file, 'rb')}
        response = requests.post(
            url=f"{self.url}/files",
            files=file_to_upload,
        )
        if response.ok:
            return FileDatabaseEntry(**response.json())
        else:
            raise ValueError(
                f"API could not be accessed. "
                f"Response error code {response.status_code}",
            )

    def download_file(self, file_id: str, path_to_save: Path):
        response = requests.get(f"{self.url}/files/{file_id}")

        content_type = response.headers["content-type"].split("/")[0]
        # TODO: process content type more clearly
        filename = \
            response.headers["content-disposition"].\
                split("filename=")[-1].\
                replace('"', '')

        # TODO: can anything that isn't an image be sent to API

        if content_type == 'image':
            with open(path_to_save / filename, "wb") as file:
                file.write(response.content)
        else:
            raise NotImplementedError("This api only handles images.")

    def delete_file(self, file_id: str) -> FileDatabaseEntry:
        """Deletes file and corresponding entry in database."""
        response = requests.delete(url=f"{self.url}/files/{file_id}")
        if response.ok:
            response = response.json()
            return FileDatabaseEntry(
                file_id=response["file_id"],
                metadata=response["metadata"]
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
                metadata=response["metadata"]
            )
        else:
            raise ValueError
