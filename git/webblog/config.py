import os

CSRF = True
SECRET_KEY = 'ohmidog'
basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

