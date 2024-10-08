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
        """
        A database synchronizer that handles concurrency using either threads or processes.
        :param filename: The name of the file to use for the database.
        :param state: SyncState specifying whether to use threads or processes.
        :param max_readers: Maximum number of concurrent readers.
        :param database: Optional database object to initialize the FileDB superclass.
        :return: None
        """
        super().__init__(filename,database)
        self.state = state

        if state == SyncState.THREADS:
            self.read_lock = threading.Semaphore(max_readers)
            self.write_lock = threading.Lock()
        elif state == SyncState.PROCESSES:
            self.read_lock = multiprocessing.Semaphore(max_readers)
            self.write_lock = multiprocessing.Lock()
        else:
            raise Exception("invalid state")

    def get_value(self, key):
        """
        Retrieves a value from the database by key.
        :param key: The key for which the value is requested.
        :return: The value associated with the provided key.
        """
        with self.read_lock:
            self.write_lock.acquire()
            self.write_lock.release()
            super().load_file()
            results = super().get_value(key)

        return results

    def set_value(self, key, value):
        """
        Sets a value in the database for the specified key.
        :param key: The key for which the value is to be set.
        :param value: The value to set in the database.
        :return: The result of setting the value.
        """
        with self.write_lock:
            with self.read_lock:
                super().load_file()
                results = super().set_value(key, value)
                super().dump_file()

        return results

    def delete_value(self, key):
        """
        Deletes a value from the database for the specified key.
        :param key: The key for which the value is to be deleted.
        :return: The result of deleting the value.
        """
        with self.write_lock:
            with self.read_lock:
                super().load_file()
                results = super().delete_value(key)
                super().dump_file()

        return results
