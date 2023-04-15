import os
import razorpay

from flask import Flask
from flask_mysqldb import MySQL
from flask_sse import sse
from config import MYSQL_DATABASE, MYSQL_HOST, PASSWORD, MYSQL_USER, RAZORPAY_API_KEY, RAZORPAY_API_SECRET


def create_app():
    app = Flask(__name__, template_folder='../templates',
                static_folder='../static')
    # Configure db
    app.config['MYSQL_HOST'] = MYSQL_HOST
    app.config['MYSQL_USER'] = MYSQL_USER
    app.config['MYSQL_PASSWORD'] = PASSWORD
    app.config['MYSQL_DB'] = MYSQL_DATABASE
    app.secret_key = os.urandom(24)
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # 1 day in seconds
    app.register_blueprint(sse, url_prefix='/stream')

    razorpay_client = razorpay.Client(
        auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))

    mysql = MySQL(app)
    return app, mysql, razorpay_client
