import threading

from database.synchronizer_db import SynchronizerDB, SyncState


FILENAME = "assertions_test.pickle"
MAX_READERS = 10
THREADS_NUM = 10


def simple_db_test(sync_db):

    assert not sync_db.get_value(1)

    sync_db.set_value(1, True)
    assert sync_db.get_value(1)

    assert sync_db.delete_value(1)

    assert sync_db.get_value(1) is None


def assert_synchronizer_threads():
    sync_db = SynchronizerDB(
        FILENAME,
        SyncState.THREADS,
        MAX_READERS,
        {1: False}
    )
    threads = []
    for i in range(THREADS_NUM):
        threads.append(threading.Thread(target=simple_db_test,args=(sync_db,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    assert_synchronizer_threads()
