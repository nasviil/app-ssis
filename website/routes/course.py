from flask import Blueprint, render_template, request, flash

course = Blueprint('course', __name__)

@course.route('/')
def course_home():
    return render_template("page-course.html")

@course.route('/add', methods=['GET', 'POST'])
def add_course():
    if request.method =='POST':
        data = request.form
        print(data)
        flash('Course added.', category='success')

    return render_template("add-course.html")