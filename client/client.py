from pathlib import Path

import requests

from file_data_transfer_api.api_datamodel import FileDatabaseEntry

class Client:
    def __init__(self):
        self.url = "http://127.0.0.1:8000"

    def upload_file(self, path_to_file: Path) -> FileDatabaseEntry:
        file_to_upload = {'file': open(path_to_file, 'rb')}
        response = requests.post(url=f"{self.url}/files",files=file_to_upload)
        if response.ok:
            return FileDatabaseEntry(**response.json())
        else:
            raise ValueError

    def download_file(self, file_id: str, path_to_save: Path) -> None: # clients act as an interface to interact with apis
        response = requests.get(f"{self.url}/files/{file_id}")

        content_type = response.headers["content-type"].split("/")[0]
        filename = \
            response.headers["content-disposition"].\
                split("filename=")[-1].\
                replace('"', '')
        if content_type == 'image':
            with open(path_to_save / filename, "wb") \
                    as file:
                file.write(response.content)
        else:
            raise NotImplementedError("This api only handles images")

    def delete_file(self, file_id: str):
        response = requests.delete(url=f"{self.url}/files/{file_id}")
        if response.ok:
            return response.json()
        else:
            raise ValueError

    def update_filename(self, file_id: str, new_filename: str):
        response = requests.put(url=f"{self.url}/files/{file_id}?newFilename={new_filename}")

        if response.ok:
            return response.json()
        else:
            raise ValueError
