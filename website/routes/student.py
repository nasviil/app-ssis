from flask import Blueprint, render_template, request, flash

student = Blueprint('student', __name__)

@student.route('/')
def student_home():
    return render_template("page-student.html")

@student.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method =='POST':
        data = request.form
        print(data)
        flash('Student added.', category='success')

    return render_template("page-student.html")