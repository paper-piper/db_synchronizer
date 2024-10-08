import threading
from logging_utils import setup_logger
from database.synchronizer_db import SynchronizerDB, SyncState

logger = setup_logger('threading_test')


FILENAME = "assertions_test.pickle"
MAX_READERS = 10
THREADS_NUM = 10


def simple_db_test(sync_db, index):
    """
    a simple set of instructions for the database
    :param sync_db:
    :param index:
    :return: None
    """

    results = sync_db.get_value(index)
    logger.info(f"on thread {index} first value = {results}")
    assert not results

    sync_db.set_value(index, True)
    results = sync_db.get_value(index)
    logger.info(f"on thread {index} seconds value = {results}")
    assert results

    assert sync_db.delete_value(index)

    assert sync_db.get_value(index) is None


def assert_synchronizer_threads():
    """
    make multiple threads run the same simple db assertion at the same time.
    :return: None
    """
    db = {}
    for i in range(THREADS_NUM):
        db[i] = False
    sync_db = SynchronizerDB(
        FILENAME,
        SyncState.THREADS,
        MAX_READERS,
        db
    )
    threads = []
    for i in range(THREADS_NUM):
        threads.append(threading.Thread(target=simple_db_test, args=(sync_db, i)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    assert_synchronizer_threads()
