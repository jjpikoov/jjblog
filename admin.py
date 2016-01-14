from flask import Blueprint, render_template, request, session,\
         redirect, url_for
import functools

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
            notification = Notification(
                    True,
                    "Login required!",
                    "Please log in to continue",
                    'warning')
            session['notification'] = notification.__dict__
            return redirect(url_for('admin.show_admin_menu_with_login'))
    return checker


class Notification():
    def __init__(
            self, active=False, title=None, description=None, color=None):
        self.active = active
        self.title = title
        self.description = description
        self.color = color


@admin.record
def record_params(setup_state):
    app = setup_state.app
    admin.config = dict(
            [(key, value) for (key, value) in app.config.iteritems()])


@admin.route('/', methods=['GET', 'POST'])
def show_admin_menu_with_login():
    if request.method == 'POST':
        notification = Notification()
        if (request.form['login'] != admin.config['USERNAME'] or
                request.form['password'] != admin.config['PASSWORD']):
            notification.active = True
            notification.color = 'alert'
            notification.title = "Authorization failed!"
            notification.description = "Wrong login or password."
        else:
            session['logged_in'] = True
            notification.active = True
            notification.color = 'success'
            notification.title = 'Successful authorization!'
            notification.description = "Welcome my admin."
        session['notification'] = notification.__dict__
    if 'notification' in session.keys():
        notification = session['notification']
        session.pop('notification', None)
    else:
        notification = Notification().__dict__
    return render_template('admin/menu.j2', notification=notification)


@admin.route('posts')
@login_required
def show_admin_posts():
    return render_template('admin/posts.j2')


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
    notification = Notification(
            True,
            "Successful logout!",
            "You have successfully logged out.",
            "secondary")
    session['notification'] = notification.__dict__
    return redirect(url_for('admin.show_admin_menu_with_login'))
