from file_db import FileDB
from logging_utils import setup_logger
from enum import Enum, auto


# Setup logger for file
logger = setup_logger('db_synchronizer')


class SyncState(Enum):
    THREADS = 0
    PROCESSES = 1


class DbSynchronizer:
    pass

