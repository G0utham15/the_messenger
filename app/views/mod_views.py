from flask import Blueprint, render_template, request, redirect, url_for
from flask_security import login_required, current_user
from flask import current_app as app
from flask_admin.base import MenuLink

mod_blueprint = Blueprint('mods', __name__, template_folder='templates')

@mod_blueprint.route("/")
def index():
    return render_template('mod/index.html')

@mod_blueprint.route("/user")
def users():
    return render_template('mod/users.html')

@mod_blueprint.route("/profile")
def profile():
    return render_template('mod/profile.html')
