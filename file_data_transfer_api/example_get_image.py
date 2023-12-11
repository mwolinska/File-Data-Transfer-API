from typing import Dict, Any

import requests


class QueryBuilder:
    def get_file(self, file_id: str, return_file_info: bool = True) -> Dict[str, Any]: # clients act as an interface to interact with apis
        response = requests.get(f"http://127.0.0.1:8000/files/{file_id}?return_file_info={return_file_info}")
        if response.ok:
            return response.json()
        else:
            raise ValueError

# class ReturnFileInfo(str, Enum):


if __name__ == '__main__':

    client = QueryBuilder(
        # auth
    )
    response = client.get_file(file_id="6d332065-c782-490a-97cf-ba2b05e8ad88",
                                         return_file_info=False, )
