from database import Database
import json
from logging_utils import setup_logger

# Setup logger for file
logger = setup_logger('file_db')


class FileDB(Database):

    def __init__(self, filename, database=None):
        super().__init__(database)
        self.filename = filename

    def save_file(self):
        """
        Writes the current database to a file in JSON format.
        :return: True if the operation is successful, False otherwise.
        """
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.db, f)
            logger.info(f"Database successfully written to file")
            return True
        except Exception as e:
            logger.error(f"Failed to write database to file : {e}")
            return False

    def update_file(self):
        """
        Reads a database from a file in JSON format and loads it into the current database.
        :return: True if the operation is successful, False otherwise.
        """
        try:
            with open(self.filename, 'r') as f:
                self.db = json.load(f)
            logger.info(f"Database successfully loaded")
            return True
        except FileNotFoundError:
            logger.error(f"File '{self.filename}' not found.")
            return False
        except Exception as e:
            logger.error(f"Failed to read database from file '{self.filename}': {e}")
            return False


def assert_file_db():
    file_db = FileDB("test.json", {"test": 1, "another value": 0})
    file_db.save_file()
    assert file_db.get_value("test") == 1

    file_db.delete_value("test")
    file_db.save_file()

    file_db_2 = FileDB("test.json")
    file_db_2.update_file()
    assert not file_db_2.get_value("test")


if __name__ == "__main__":
    assert_file_db()
