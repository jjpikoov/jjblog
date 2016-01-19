from flask import Flask, g, render_template
from admin import admin
from database import SqliteDatabase

app = Flask(__name__)
app.config.from_object('config.DevConfig')


database = SqliteDatabase(app.config['DATABASE'])
database.init_db()

app.register_blueprint(admin, url_prefix='/admin/')


@app.before_request
def before_request():
    """
    Operations done before each request.
    """
    app.config['BLOG_NAME'] = admin.config['BLOG_NAME']
    g.db = database
    g.db.connect_db()


@app.teardown_request
def teardown_request(exception):
    """
    Operations on teardown.
    """
    db = getattr(g, 'db', None)
    db.close_db()


@app.route('/')
def show_blog():
    """
    Fuction for "host/".
    Main functions which shows all posts and widgets.
    """
    posts = g.db.get_posts()
    widgets = g.db.get_widgets()
    return render_template('blog.j2', posts=posts, widgets=widgets)


if __name__ == '__main__':
    app.run()
