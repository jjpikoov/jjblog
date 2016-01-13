import sqlite3
from flask import Flask, g, redirect, url_for
from contextlib import closing
from admin import admin

app = Flask(__name__)
app.config.from_object('config.DevConfig')


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

app.register_blueprint(admin, url_prefix='/admin/')


@app.route('/')
def show_blog():
    return redirect(url_for('admin.show_admin_menu_with_login'))
    # return render_template('blog.j2')


if __name__ == '__main__':
    app.run()
