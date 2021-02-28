from flask import Blueprint, render_template, request, redirect, url_for
from flask_security import login_required, current_user
from flask import current_app as app
from flask_admin.base import MenuLink

biz_blueprint = Blueprint('Business', __name__, template_folder='templates')

@biz_blueprint.route("/")
def index():
    return render_template('business/index.html')

