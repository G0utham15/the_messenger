import os.path as op

from flask import Flask
from flask_admin import Admin
from flask_admin.base import MenuLink
from flask_admin.contrib.fileadmin import FileAdmin
from flask_admin.contrib.mongoengine import ModelView
from flask_babelex import Babel
#from flask_mail import Mail
from flask_migrate import Migrate
from flask_mongoengine import MongoEngine
from flask_security import MongoEngineUserDatastore, Security, current_user
from app.forms import registerForm
from flask_wtf.csrf import CSRFProtect


# Forms

# Instantiate Flask extensions
db = MongoEngine()
csrf_protect = CSRFProtect()
#mail = Mail()
migrate = Migrate()
babel = Babel()
security = Security()

def create_app(extra_config_settings={}):
    # Create a Flask applicaction.

    # Instantiate Flask
    app = Flask(__name__)

    # Load App Config settings
    # Load common settings from 'app/settings.py' file
    app.config.from_object('app.settings')
    # Load local settings from 'app/local_settings.py'
    app.config.from_object('app.local_settings')
    # Load extra config settings from 'extra_config_settings' param
    app.config.update(extra_config_settings)

    # Setup db Mongo
    db.init_app(app)

    # Setup Flask-Mail
    #mail.init_app(app)

    # Setup WTForms CSRFProtect
    csrf_protect.init_app(app)

    # Register blueprints
    from app.views.public_views import public_blueprint
    app.register_blueprint(public_blueprint)
    from app.views.success import members_blueprint
    app.register_blueprint(members_blueprint)
    from app.views.admin_views import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    from app.views.mod_views import mod_blueprint
    app.register_blueprint(mod_blueprint, url_prefix='/mod')
    from app.views.biz_views import biz_blueprint
    app.register_blueprint(biz_blueprint, url_prefix='/biz')
    # Setup an error-logger to send emails to app.config.ADMINS
    #init_email_error_handler(app)

    # Setup Flask-secure
    from .models.user_models import Role, User
    app.user_datastore = MongoEngineUserDatastore(db, User, Role)
    security.init_app(app, app.user_datastore, register_form=registerForm)
    # datastore.create_user(email='matt@nobien.net', password='password')

    babel.init_app(app)  # Initialize flask_babelex

    # Setup Flask-admin
    class AdminUserView(ModelView):
        can_create = False
        column_exclude_list = ('password')
        column_editable_list=['active']
        def is_accessible(self):
            return current_user.has_role('admin')


    adminDash = Admin(app, name='admin', template_mode='bootstrap4',url="/admin", endpoint='admin')#, index_view=adminView(url='/admin', endpoint='admin'))
    adminDash.add_view(AdminUserView(User))
    adminDash.add_view(ModelView(Role))
    path = op.join(op.dirname(__file__), './')
    adminDash.add_view(FileAdmin(path, '/', name='Files'))
    adminDash.add_link(MenuLink(name='Profile', endpoint='members.member_page'))
    adminDash.add_link(MenuLink(name='Logout', endpoint='security.logout'))
    return app

'''
def init_email_error_handler(app):
    # Initialize a logger to send emails on error-level messages.
    # Unhandled exceptions will now send an email message to app.config.ADMINS.
    if app.debug:
        return  # Do not send error emails while developing

    # Retrieve email settings from app.config
    host = app.config['MAIL_SERVER']
    port = app.config['MAIL_PORT']
    from_addr = app.config['MAIL_DEFAULT_SENDER']
    username = app.config['MAIL_USERNAME']
    password = app.config['MAIL_PASSWORD']
    secure = () if app.config.get('MAIL_USE_TLS') else None

    # Retrieve app settings from app.config
    to_addr_list = app.config['ADMINS']
    subject = app.config.get('APP_SYSTEM_ERROR_SUBJECT_LINE', 'System Error')

    # Setup an SMTP mail handler for error-level messages
    import logging
    from logging.handlers import SMTPHandler

    mail_handler = SMTPHandler(
        mailhost=(host, port),  # Mail host and port
        fromaddr=from_addr,  # From address
        toaddrs=to_addr_list,  # To address
        subject=subject,  # Subject line
        credentials=(username, password),  # Credentials
        secure=secure,
    )

    # Log errors using: app.logger.error('Some error message')
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)
'''
