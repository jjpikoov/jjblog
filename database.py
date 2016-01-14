import os
import sqlite3


class Database():
    def __init__():
        raise NotImplementedError()

    def connect_db():
        raise NotImplementedError()

    def init_db():
        raise NotImplementedError()

    def get_connection():
        raise NotImplementedError()


class SqliteDatabase(Database):
    def __init__(self, db_file):
        self.db_file = db_file

    def connect_db(self):
        self.db = sqlite3.connect(self.db_file)

    def close_db(self):
        if self.db is not None:
            self.db.close()

    def init_db(self):
        # Some logger here???
        if not os.path.isfile(self.db_file):
            self.connect_db()
            with open('schema.sql', 'rt') as f:
                schema = f.read()
            self.db.cursor().executescript(schema)
            self.db.close()
