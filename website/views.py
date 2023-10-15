from flask import Blueprint, render_template, redirect, url_for, request, flash

views = Blueprint('views', __name__)

@views.route('/student')
def student():
    return render_template("student.html")

@views.route('/course')
def course():
    return render_template("course.html")

@views.route('/college')
def college():
    return render_template("college.html")

@views.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method =='POST':
        data = request.form
        print(data)
        flash('Student added.', category='success')

    return render_template("student-add.html")

@views.route('/course/add', methods=['GET', 'POST'])
def add_course():
    return render_template("course-add.html")

@views.route('/college/add', methods=['GET', 'POST'])
def add_college():
    return render_template("college-add.html")

@views.route('/')
def index():
    return redirect(url_for('views.student'))