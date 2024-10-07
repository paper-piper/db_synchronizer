from file_db import FileDB
from logging_utils import setup_logger
from enum import Enum
import threading
import multiprocessing


# Setup logger for file
logger = setup_logger('db_synchronizer')


class SyncState(Enum):
    THREADS = 0
    PROCESSES = 1


class DbSynchronizer(FileDB):
    def __init__(self, filename, state, max_readers = 10, database=None):
        super().__init__(filename,database)
        self.state = state

        if state == SyncState.THREADS:
            self.read_lock = threading.Semaphore(max_readers)
            self.write_lock = threading.Lock()
        elif state == SyncState.PROCESSES:
            self.read_lock = multiprocessing.Semaphore(max_readers)
            self.write_lock = multiprocessing.Lock()
        else:
            raise Exception("Did not enter valid state")


    def get_value(self,key):
        with self.read_lock:
            super().load_file()
            results =  super().get_value(key)

        return results


    def set_value(self, key, value):
        with self.write_lock:
            super().load_file()
            results = super().set_value(key,value)
            super().dump_file()

        return results

    def delete_value(self, key):
        with self.write_lock:
            super().load_file()
            results = super().delete_value(key)
            super().dump_file()

        return results

