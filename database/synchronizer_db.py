from database.file_db import FileDB
from logging_utils import setup_logger
from enum import Enum
import threading
import multiprocessing


# Setup logger for file
logger = setup_logger('synchronizer_db')


class SyncState(Enum):
    THREADS = 0
    PROCESSES = 1


class SynchronizerDB(FileDB):
    def __init__(self, filename, state, max_readers=10, database=None):
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

    def get_value(self, key):
        # for debug purpose, check if the lock is free and debug
        if self.read_lock.acquire(blocking=False):
            logger.info("Read lock is already in use, waiting for release")
            self.read_lock.release()
        else:
            logger.info("Read lock is Free, using it")
        with self.read_lock:
            super().load_file()
            results = super().get_value(key)

        return results

    def set_value(self, key, value):
        logger.info("Hallooo")
        if self.write_lock.locked():
            logger.info("Write lock is already in use, waiting for release")
        else:
            logger.info("Write lock is Free, using it")
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
