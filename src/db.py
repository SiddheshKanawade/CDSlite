import os

from flask import Flask
from flask_mysqldb import MySQL

from config import MYSQL_DATABASE, MYSQL_HOST, PASSWORD, MYSQL_USER


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    # Configure db
    app.config['MYSQL_HOST'] = MYSQL_HOST
    app.config['MYSQL_USER'] = MYSQL_USER
    app.config['MYSQL_PASSWORD'] = PASSWORD
    app.config['MYSQL_DB'] = MYSQL_DATABASE
    app.secret_key = os.urandom(24)
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400 # 1 day in seconds
    mysql = MySQL(app)

    return app, mysql
