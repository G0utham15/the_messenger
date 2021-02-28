from datetime import timedelta
import os

# *****************************
# Environment specific settings
# *****************************

# DO NOT use "DEBUG = True" in production environments
DEBUG = True

# DO NOT use Unsecure Secrets in production environments
# Generate a safe one with:
#    python -c "import os; print(repr(os.urandom(24)));"
SECRET_KEY = 'V\xd4\x17\x04\xf4\xa4\x06$s\x14\x0b3X\xf8?\xd6\x11\xb5_Q\xdawq\xb7'
COOKIE_SECURE = 'Secure'
COOKIE_DURATION = timedelta(days=30)
SECURITY_TOKEN_MAX_AGE=120

# MongoDB Config
MONGODB_DB = 'auth'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

# Flask Security
SECURITY_PASSWORD_SALT = '\xc1\x1cWSU\xff\xe5p_\x97;|\xd7I\xd5\x8f\xa7\x7f@\xb7[4\x00\\'
SECURITY_REGISTERABLE = True
SECURITY_RECOVERABLE = False
SECURITY_CHANGEABLE = True
SECURITY_USER_IDENTITY_ATTRIBUTES=['email', 'username']
SECURITY_SEND_REGISTER_EMAIL=False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL=False

# i18n
BABEL_TRANSLATION_DIRECTORIES = os.path.join(os.path.abspath(
    os.path.dirname(__file__)), 'translations/')

BABEL_DEFAULT_LOCALE = 'en'

# Flask-Mail settings
# For smtp.gmail.com to work, you MUST set "Allow less secure apps"
# to ON in Google Accounts.
# Change it in https://myaccount.google.com/security#connectedapps
# (near the bottom).
SECURITY_POST_LOGIN_VIEW= 'members.member_page'
SECURITY_POST_LOGOUT_VIEW= 'security.login'

'''
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_SSL = False
MAIL_USE_TLS = True
MAIL_USERNAME = 'yourname@gmail.com'
MAIL_PASSWORD = 'password'
MAIL_DEFAULT_SENDER = '"Your Name" <yourname@gmail.com>'

ADMINS = [
    '"Admin One" <admin1@gmail.com>',
]
'''