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
        if not os.path.isfile(self.db_file):
            self.connect_db()
            with open('schema.sql', 'r') as f:
                schema = f.read()
                self.db.cursor().executescript(schema)
            self.db.commit()
            self.db.close()

    def add_post(self, title, date, text):
        self.db.cursor().execute(
                "INSERT INTO posts (title, date, text)\
                VALUES(?, ?, ?)", [title, date, text])
        self.db.commit()

    def get_posts(self):
        posts = []
        for row in self.db.cursor().execute(
                "SELECT id, title, date, text FROM posts ORDER BY id DESC"):
            text = row[3]
            if len(text) > 100:
                text = text[:100] + "..."
            posts.append(dict(
                        post_id=str(row[0]),
                        title=row[1], date=row[2], text=text))
        return posts

    def get_post_by_id(self, post_id):
        for post in self.db.cursor().execute(
                "SELECT id, title, date, text FROM posts WHERE id = ?",
                post_id):
            return dict(
                    post_id=str(post[0]),
                    title=post[1], date=post[2], text=post[3])

    def delete_post(self, post_id):
        self.db.cursor().execute(
                "DELETE FROM posts WHERE id = ?", str(post_id))
        self.db.commit()

    def edit_post(self, post_id, title, date, text):
        self.db.cursor().execute(
                "UPDATE posts SET title = ?, date = ?, text = ?\
                WHERE id = ?", [title, date, text, post_id])
        self.db.commit()
