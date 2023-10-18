from flask import Flask
from os import getenv
from flask_mysql_connector import MySQL

from .db import create_tables, mysql
from website.config import Config

from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)
    app.config['SECRET_KEY']=getenv('SECRET_KEY')

    create_tables(app=app, mysql=mysql)

    from .routes.home import home
    from .routes.student import student
    from .routes.course import course
    from .routes.college import college

    app.register_blueprint(home,url_prefix='/')
    app.register_blueprint(student,url_prefix='/student')
    app.register_blueprint(course,url_prefix='/course')
    app.register_blueprint(college,url_prefix='/college')

    return app