from flask import Blueprint, render_template, request, session,\
         redirect, url_for, g
import functools
from util import validate_date

admin = Blueprint('admin', __name__)


def login_required(func):
    @functools.wraps(func)
    def checker(*args):
        if 'logged_in' in session.keys() and session['logged_in']:
            if args == ():
                return func()
            else:
                return func(args)
        else:
            session['notification_active'] = True
            session['notification_title'] = "Login required"
            session['notification_description'] = "Please log in to continue"
            session['notification_color'] = "warning"
            return redirect(url_for('admin.show_admin_menu_with_login'))
    return checker


def throw_notification_once(func):
    @functools.wraps(func)
    def wrapper(*args):
        if args == ():
            retval = func()
        else:
            retval = func(args)
        session['notification_active'] = False
        return retval
    return wrapper


@admin.record
def record_params(setup_state):
    app = setup_state.app
    admin.config = dict(
            [(key, value) for (key, value) in app.config.iteritems()])


@admin.route('/', methods=['GET', 'POST'])
@throw_notification_once
def show_admin_menu_with_login():
    if request.method == 'POST':
        if (request.form['login'] != admin.config['USERNAME'] or
                request.form['password'] != admin.config['PASSWORD']):
            session['notification_active'] = True
            session['notification_color'] = 'alert'
            session['notification_title'] = "Authorization failed!"
            session['notification_description'] = "Wrong login or password."
        else:
            session['logged_in'] = True
            session['notification_active'] = True
            session['notification_color'] = 'success'
            session['notification_title'] = 'Successful authorization!'
            session['notification_description'] = "Welcome my admin."

    return render_template('admin/menu.j2')


@admin.route('posts')
@login_required
def show_admin_posts():
    return render_template('admin/posts.j2')


@admin.route('posts/new', methods=['GET', 'POST'])
@login_required
def show_new_post_forms():
    if request.method == 'POST':
        day = request.form['day'],
        month = request.form['month'],
        year = request.form['year']
        if validate_date(day, month, year):
            date = day + "." + month + "." + year
            g.db.add_post(
                request.form['title'],
                date,
                request._form['text'])
            return url_for('admin.show_admin_posts')
        else:
            pass
    return render_template('admin/new_post.j2')


@admin.route('widgets')
@login_required
def show_admin_widgets():
    return "Admin widgets"


@admin.route('settings')
@login_required
def show_admin_settings():
    return "Admin settings"


@admin.route('logout')
def logout():
    session.pop('logged_in', None)
    session['notification_active'] = True
    session['notification_title'] = "Successful logout!"
    session['notification_description'] = "You have successfully logged out."
    session['notification_color'] = "secondary"
    return redirect(url_for('admin.show_admin_menu_with_login'))
