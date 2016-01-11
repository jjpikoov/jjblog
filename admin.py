from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)


@admin.route('/')
def show_admin_menu():
    return render_template('admin/menu.j2')


@admin.route('posts')
def show_admin_posts():
    return "admin_posts"


@admin.route('widgets')
def show_admin_widgets():
    return "Admin widgets"


@admin.route('settings')
def show_admin_settings():
    return "Admin settings"
