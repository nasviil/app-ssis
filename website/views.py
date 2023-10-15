from flask import Blueprint, render_template, redirect, url_for

views = Blueprint('views', __name__)

@views.route('/student')
def student():
    return render_template("student.html")

@views.route('/course')
def course():
    return render_template("course.html")

@views.route('/')
def index():
    return redirect(url_for('views.student'))