from pathlib import Path


from database_client.database_connection.local_database_connection import \
    LocalJsonDatabaseConnection
from database_client.datamodel.database_entry import FileDatabaseEntry
from database_client.env_variables import DATABASE_PATH


class DatabaseManager:
    @staticmethod
    def _select_database():
        uri = Path(DATABASE_PATH).as_uri()
        # TODO: decouple database handling from file handling
        if "file://" in uri:
            return LocalJsonDatabaseConnection()
        else:
            raise NotImplementedError(
                "This upload_path does not correspond to a known file system."
            )

    @classmethod
    def add_entry(cls, entry: FileDatabaseEntry):
        database = cls._select_database()
        return database.add_new_entry(entry=entry)

    @classmethod
    def update_entry(cls, database_entry: FileDatabaseEntry):
        database = cls._select_database()
        return database.update_entry(
            updated_entry=database_entry)

    @classmethod
    def retrieve_entry(cls, item_id: str) -> FileDatabaseEntry:
        database = cls._select_database()
        return database.retrieve_entry(item_id=item_id)

    @classmethod
    def delete_entry(cls, item_id: str) -> FileDatabaseEntry:
        database = cls._select_database()
        return database.delete_entry(item_id=item_id)
