# File-Data-Transfer-API
This project contains a simple API designed to upload and download files. 

## Installation
```
git clone https://github.com/mwolinska/File-Data-Transfer-API
cd File-Data-Transfer-API
```
This package uses [poetry](https://python-poetry.org) dependency manager. 
To install all dependencies run:

```bash
poetry install
```

## Getting Started

This API currently contains four functionalities:
* Uploading a file,
* Downloading a (previously uploaded) file,
* Renaming an uploaded file,
* Deleting a file.

To use our API we recommend using our client. 
To access the functionalities, first instanstiate a `Client`.

```python
from client import Client
from pathlib import Path

client = Client()

```
To upload a file, simply pass the desired path to your file:

```python
import pathlib

uploaded_file_metadata = client.upload_file(
    path_to_file=pathlib.Path("path/to/your/file"),
)
```
For the rest of the functionalities you will need the `file_id`. 
To run our demo, use the `file_id` below:
```python
file_id = "<desired-file-id>"
file_id = "66b2dcfb-06be-4d7d-a8d0-6f0f34710562"
```

To download a demo file set the desired `file_id`. 
To download our demo image use the `file_id` below.
```python
client.download_file(
    file_id=file_id,
    path_to_save="<path-to-save-file>",
)
```
To update the filename: 
```python
updated_entry = client.update_filename(
    file_id=file_id,
    new_filename="<new-filename>",
)
```

To remove an entry from the databse run:
```python
deleted_entry = client.delete_file(file_id=file_id)
```
