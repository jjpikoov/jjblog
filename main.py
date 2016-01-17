from flask import Flask, g, render_template
from admin import admin
from database import SqliteDatabase

app = Flask(__name__)
app.config.from_object('config.DevConfig')


database = SqliteDatabase(app.config['DATABASE'])
database.init_db()


@app.before_request
def before_request():
    g.db = database
    g.db.connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    db.close_db()

app.register_blueprint(admin, url_prefix='/admin/')


@app.route('/')
def show_blog():
    posts = g.db.get_posts()
    return render_template('blog.j2', posts=posts)


if __name__ == '__main__':
    app.run()
