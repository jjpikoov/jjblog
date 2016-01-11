from flask import Blueprint, render_template

admin = Blueprint('admin', __name__)


@admin.route('/')
def show_admin_menu():
    return render_template('admin/menu.j2')
