from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET KEY']='super secret key'

    from .routes.home import home
    from .routes.student import student
    from .routes.course import course
    from .routes.college import college

    app.register_blueprint(home,url_prefix='/')
    app.register_blueprint(student,url_prefix='/student')
    app.register_blueprint(course,url_prefix='/course')
    app.register_blueprint(college,url_prefix='/college')

    return app