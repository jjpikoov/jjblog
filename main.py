from flask import Flask, g, redirect, url_for
from admin import admin
from database import SqliteDatabase
from util import Notification

app = Flask(__name__)
app.config.from_object('config.DevConfig')


database = SqliteDatabase(app.config['DATABASE'])
database.init_db()

# with app.app_context():
#     g.notification = Notification()
#     print(">>>>>")
#     print(g.notification)
#     print(">>>>>")


# @app.before_first_request
# def before_first_request():
#     g.notification = Notification()


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
    return redirect(url_for('admin.show_admin_menu_with_login'))
    # return render_template('blog.j2')


if __name__ == '__main__':
    app.run()
