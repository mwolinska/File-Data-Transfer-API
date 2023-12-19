from abc import ABC, abstractmethod

from database_client.datamodel.database_entry import FileDatabaseEntry


class AbstractDatabaseConnection(ABC):

    @abstractmethod
    def add_new_entry(self, entry: FileDatabaseEntry):
        pass

    @abstractmethod
    def update_entry(self, updated_entry: FileDatabaseEntry):
        pass

    @abstractmethod
    def retrieve_entry(self, id: str) -> FileDatabaseEntry:
        pass

    @abstractmethod
    def delete_entry(self, id: str) -> FileDatabaseEntry:
        pass
