from flask import Blueprint, render_template, request, redirect, url_for
from flask_security import login_required, current_user
from flask_admin import AdminIndexView, expose
from app import babel
from flask import current_app as app
import gettext

admin_blueprint = Blueprint('admins', __name__, template_folder='templates/admin')

class adminView(AdminIndexView):
    @expose('/')
    def index(self):
        return 'Hello From first admin :{}.'.format(self)