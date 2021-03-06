import re

from flask import Blueprint, g, redirect, render_template, request, session, \
    url_for
from util import validate_date

import functools


admin = Blueprint('admin', __name__)


def login_required(func):
    """
    Decorator which redirect to admin's menu page
    if user is not logged in.
    """
    @functools.wraps(func)
    def checker(**kwargs):
        if 'logged_in' in session.keys() and session['logged_in']:
            if kwargs == {}:
                return func()
            else:
                return func(*kwargs.values())
        else:
            session['notification_active'] = True
            session['notification_title'] = "Login required!"
            session['notification_description'] = "Please log in to continue."
            session['notification_color'] = "warning"
            return redirect(url_for('admin.show_admin_menu_with_login'))
    return checker


def throw_notification_once(func):
    """
    Decorator which executes given function and after that
    sets session's notifcation to non-active.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if args == ():
            retval = func()
        else:
            retval = func(args)
        if type(retval).__name__ == "unicode":
            session['notification_active'] = False
        return retval
    return wrapper


@admin.record
def record_params(setup_state):
    """
    Function copies config from app to admin object.
    """
    app = setup_state.app
    admin.config = dict(
            [(key, value) for (key, value) in app.config.iteritems()])


@admin.route('/', methods=['GET', 'POST'])
@throw_notification_once
def show_admin_menu_with_login():
    """
    Main function for "host/admin/
    """
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

    return render_template('admin/menu.djhtml')


@admin.route('posts')
@login_required
@throw_notification_once
def show_admin_posts():
    """
    Function for "host/admin/posts".
    Shows all posts.
    """
    posts = g.db.get_posts()
    for post in posts:
        if len(post['text']) > 100:
            post['text'] = post['text'][:100] + "..."
    return render_template('admin/posts.djhtml', posts=posts)


@admin.route('posts/new', methods=['GET', 'POST'])
@login_required
@throw_notification_once
def show_new_post_forms():
    """
    Function for "host/admin/posts/new".
    Creator of new posts.
    """
    if request.method == 'POST':
        day = int(request.form['day'])
        month = int(request.form['month'])
        year = int(request.form['year'])
        if validate_date(day, month, year):
            date = str(day) + "." + str(month) + "." + str(year)
            g.db.add_post(
                request.form['title'],
                date,
                request.form['text'])
            session['notification_active'] = True
            session['notification_title'] = "Post created!"
            session['notification_description'] = "Post successfully created."
            session['notification_color'] = "success"
            return redirect(url_for('admin.show_admin_posts'))
        else:
            session['notification_active'] = True
            session['notification_title'] = "Date error!"
            session['notification_color'] = "alert"
            session['notification_description'] = "Please check date form\
                twice."
    return render_template('admin/new_post.djhtml')


@admin.route('posts/delete/<int:post_id>')
@login_required
def delete_post(post_id):
    """
    Function for deleting post with given post_id.
    """
    g.db.delete_post(post_id)
    return redirect(url_for('admin.show_admin_posts'))


@admin.route('posts/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
@throw_notification_once
def edit_post(post_id):
    """
    Function for editing existing post.
    """
    if request.method == 'POST':
        day = int(request.form['day'])
        month = int(request.form['month'])
        year = int(request.form['year'])
        if validate_date(day, month, year):
            date = str(day) + "." + str(month) + "." + str(year)
            g.db.edit_post(
                    post_id[0],
                    request.form['title'],
                    date,
                    request.form['text'])
            return redirect(url_for('admin.show_admin_posts'))
        else:
            session['notification_active'] = True
            session['notification_title'] = "Date error!"
            session['notification_color'] = "alert"
            session['notification_description'] = "Please check date form\
                twice."
    post = g.db.get_post_by_id(post_id)
    date = re.split(r'\.', post['date'])
    post['day'] = date[0]
    post['month'] = date[1]
    post['year'] = date[2]
    return render_template('admin/edit_post.djhtml', post=post)


@admin.route('widgets')
@login_required
@throw_notification_once
def show_admin_widgets():
    """
    Function for "host/admin/widgets".
    Shows all widgets.
    """
    widgets = g.db.get_widgets()
    for widget in widgets:
        if len(widget['body']) > 100:
            widget['body'] = widget['body'][:100] + "..."
    return render_template('admin/widgets.djhtml', widgets=widgets)


@admin.route('widgets/new', methods=['GET', 'POST'])
@login_required
@throw_notification_once
def show_new_widget_forms():
    """
    Function for "host/admin/widgets/new".
    Creator of new widgets.
    """
    if request.method == 'POST':
        g.db.add_widget(
                request.form['name'],
                request.form['body'])

        session['notification_active'] = True
        session['notification_title'] = "Widget  created!"
        session['notification_description'] = "Widget successfully created."
        session['notification_color'] = "success"
        return redirect(url_for('admin.show_admin_widgets'))
    return render_template('admin/new_widget.djhtml')


@admin.route('widgets/delete/<int:widget_id>')
@login_required
def delete_widget(widget_id):
    """
    Function for deleting widget with given widget_id.
    """
    g.db.delete_widget(widget_id)
    return redirect(url_for('admin.show_admin_widgets'))


@admin.route('widgets/edit/<int:widget_id>', methods=['GET', 'POST'])
@login_required
@throw_notification_once
def edit_widget(widget_id):
    """
    Function for editing existing widget.
    """
    if request.method == 'POST':
        g.db.edit_widget(
                    widget_id[0],
                    request.form['name'],
                    request.form['body'])
        return redirect(url_for('admin.show_admin_widgets'))
    widget = g.db.get_widget_by_id(widget_id)
    return render_template('admin/edit_widget.djhtml', widget=widget)


@admin.route('settings', methods=['GET', 'POST'])
@login_required
@throw_notification_once
def show_admin_settings():
    """
    Function for "/admin/settings".
    Shows all avaiable blog's settings.
    """
    if request.method == 'POST':
        admin.config['BLOG_NAME'] = request.form['blog_name']
        session['notification_active'] = True
        session['notification_title'] = "Name changed!"
        session['notification_description'] = "Name\
            has been successfully changed."
        session['notification_color'] = "success"
        return redirect(url_for('admin.show_admin_settings'))
    return render_template('admin/settings.djhtml')


@admin.route('logout')
@login_required
def logout():
    """
    Functions loggs out user and change notification.
    """
    session.pop('logged_in', None)
    session['notification_active'] = True
    session['notification_title'] = "Successful logout!"
    session['notification_description'] = "You have successfully logged out."
    session['notification_color'] = "secondary"
    return redirect(url_for('admin.show_admin_menu_with_login'))
