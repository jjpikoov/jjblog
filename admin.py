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
            return redirect(url_for('admin.show_admin_menu_with_login'))
    return checker


class AdminNotification():
    def __init__(self, active, subject, description, color):
        self.active = active
        self.subject = subject
        self.description = description
        self.color = color


@admin.record
def record_params(setup_state):
    app = setup_state.app
    admin.config = dict(
            [(key, value) for (key, value) in app.config.iteritems()])


@admin.route('/', methods=['GET', 'POST'])
def show_admin_menu_with_login():
    login_failed = False
    if request.method == 'POST':
        if (request.form['login'] != admin.config['USERNAME'] or
                request.form['password'] != admin.config['PASSWORD']):
            login_failed = True
        else:
            session['logged_in'] = True
    return render_template('admin/menu.j2', login_failed=login_failed)


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
    return redirect(url_for('admin.show_admin_menu_with_login'))
