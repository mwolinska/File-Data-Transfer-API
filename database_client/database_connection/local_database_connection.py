import json
from typing import Dict

from database_client.database_connection.abstract_databse_connection import \
    AbstractDatabaseConnection
from database_client.datamodel.database_entry import FileDatabaseEntry, \
    FileMetadata
from database_client.env_variables import DATABASE_PATH


class LocalJsonDatabaseConnection(AbstractDatabaseConnection):
    def add_new_entry(self, entry: FileDatabaseEntry):
        """Add new entry to the database.

        Args:
            entry: a file entry to be added or updated in the database.
        """
        content = self._load_database()
        content.update(entry.to_database_format())
        self._dump_to_database(content=content)

    def update_entry(self, updated_entry: FileDatabaseEntry):
        """Updates the database with an updated entry.

        Args:
            updated_entry: an entry to be added or updated in the database.
        """
        content = self._load_database()
        content.update(updated_entry.to_database_format())
        self._dump_to_database(content=content)

    def retrieve_entry(self, item_id: str) -> FileDatabaseEntry:
        """Returns file metadata based on item_id."""
        database_content = self._load_database()
        return FileDatabaseEntry(
            file_id=item_id,
            metadata=FileMetadata(**database_content[item_id]),
        )

    def delete_entry(self, item_id: str) -> FileDatabaseEntry:
        """Removes an entry from teh database.

        Args:
            item_id: unique file identifier of the file to be removed.

        Returns:
            Metadata stored against the item_id.
        """
        database_content = self._load_database()
        entry = database_content[item_id]
        del database_content[item_id]
        self._dump_to_database(content=database_content)
        return FileDatabaseEntry(
            file_id=item_id,
            metadata=FileMetadata(filename=entry["filename"])
        )

    @staticmethod
    def _load_database() -> Dict[str, str]:
        """Returns json database as dictionary."""
        with open(DATABASE_PATH, "r") as local_file:
            content = json.load(local_file)
        return content

    @staticmethod
    def _dump_to_database(content: Dict[str, str]):
        """Updates database to content.

        Args:
            content: dictionary containing all database information.
        """
        with open(DATABASE_PATH, "w") as local_file:
            json.dump(content, local_file)
