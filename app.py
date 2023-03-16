from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

from config import MYSQL_DATABASE, MYSQL_HOST, PASSWORD, MYSQL_USER

app = Flask(__name__)

# Configure db
app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = PASSWORD
app.config['MYSQL_DB'] = MYSQL_DATABASE

mysql = MySQL(app)


if __name__ == '__main__':
    app.run(debug=True)
