import os

CSRF = True
SECRET_KEY = 'ohmidog'
basedir = os.path.abspath(os.path.dirname(__file__))


DEBUG = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost:3306/flasky'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_POOL_RECYCLE = 8
