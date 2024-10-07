from file_db import FileDB
from logging_utils import setup_logger
from enum import Enum


# Setup logger for file
logger = setup_logger('db_synchronizer')


class SyncState(Enum):
    THREADS = 0
    PROCESSES = 1


class DbSynchronizer(FileDB):
    def __init__(self, filename, state, database=None):
        super().__init__(filename,database)
        self.state = state

    def get_value(self,key):
        super().load_file()
        super().get_value(key)

