import multiprocessing
from logging_utils import setup_logger
from database.synchronizer_db import SynchronizerDB, SyncState

logger = setup_logger('multiprocessing_test')

FILENAME = "assertions_test.pickle"
MAX_READERS = 10
PROCESSES_NUM = 10


def simple_db_test(sync_db, index):

    results = sync_db.get_value(index)
    logger.info(f"on process {index} first value = {results}")
    assert not results

    sync_db.set_value(index, True)
    results = sync_db.get_value(index)
    logger.info(f"on process {index} second value = {results}")
    assert results

    assert sync_db.delete_value(index)

    assert sync_db.get_value(index) is None


def assert_synchronizer_processes():
    # Multiprocessing manager to share the initial db dictionary across processes
    manager = multiprocessing.Manager()
    db = manager.dict()
    for i in range(PROCESSES_NUM):
        db[i] = False

    sync_db = SynchronizerDB(
        FILENAME,
        SyncState.PROCESSES,
        MAX_READERS,
        db
    )

    processes = []
    for i in range(PROCESSES_NUM):
        p = multiprocessing.Process(target=simple_db_test, args=(sync_db, i))
        processes.append(p)

    for process in processes:
        process.start()

    for process in processes:
        process.join()


if __name__ == "__main__":
    assert_synchronizer_processes()
