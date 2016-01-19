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
        """
        Database's file in constructor
        """
        self.db_file = db_file

    def connect_db(self):
        """
        Function establishes the connection to db.
        """
        self.db = sqlite3.connect(self.db_file)

    def close_db(self):
        """
        Function closes connection with db.
        """
        if self.db is not None:
            self.db.close()

    def init_db(self):
        """
        Function creates db file with given schema
        if doesn't exist.
        """
        if not os.path.isfile(self.db_file):
            self.connect_db()
            with open('schema.sql', 'r') as f:
                schema = f.read()
                self.db.cursor().executescript(schema)
            self.db.commit()
            self.db.close()

    def add_post(self, title, date, text):
        """
        Function for adding new posts.
        """
        self.db.cursor().execute(
                "INSERT INTO posts (title, date, text)\
                VALUES(?, ?, ?)", [title, date, text])
        self.db.commit()

    def get_posts(self):
        """
        Function for getting posts persisted in db.
        """
        posts = []
        for row in self.db.cursor().execute(
                "SELECT id, title, date, text FROM posts ORDER BY id DESC"):
            posts.append(dict(
                        post_id=str(row[0]),
                        title=row[1], date=row[2], text=row[3]))
        return posts

    def get_post_by_id(self, post_id):
        """
        Function returns post with given id.
        """
        for post in self.db.cursor().execute(
                "SELECT id, title, date, text FROM posts WHERE id = ?",
                post_id):
            return dict(
                    post_id=str(post[0]),
                    title=post[1], date=post[2], text=post[3])

    def delete_post(self, post_id):
        """
        Function removes post with given id.
        """
        self.db.cursor().execute(
                "DELETE FROM posts WHERE id = ?", str(post_id))
        self.db.commit()

    def edit_post(self, post_id, title, date, text):
        """
        Function updates post (by id).
        """
        self.db.cursor().execute(
                "UPDATE posts SET title = ?, date = ?, text = ?\
                WHERE id = ?", [title, date, text, post_id])
        self.db.commit()

    def add_widget(self, name, body):
        """
        Function for adding new widgets.
        """
        self.db.cursor().execute(
                "INSERT INTO widgets (name, body)\
                VALUES(?, ?)", [name, body])
        self.db.commit()

    def get_widgets(self):
        """
        Function for getting widgets persisted in db.
        """
        widgets = []
        for row in self.db.cursor().execute(
                "SELECT id, name, body FROM widgets"):
            widgets.append(dict(
                        widget_id=str(row[0]),
                        name=row[1], body=row[2]))
        return widgets

    def get_widget_by_id(self, widget_id):
        """
        Function returns widget with given id.
        """
        for widget in self.db.cursor().execute(
                "SELECT id, name, body FROM widgets WHERE id = ?",
                widget_id):
            return dict(
                    widget_id=str(widget[0]),
                    name=widget[1], body=widget[2])

    def delete_widget(self, widget_id):
        """
        Function removes widget with given id.
        """
        self.db.cursor().execute(
                "DELETE FROM widgets WHERE id = ?", str(widget_id))
        self.db.commit()

    def edit_widget(self, widget_id, name, body):
        """
        Function updates widget (by id).
        """
        self.db.cursor().execute(
                "UPDATE widgets SET name = ?, body = ?\
                WHERE id = ?", [name, body, widget_id])
        self.db.commit()
