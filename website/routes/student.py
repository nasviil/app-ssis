from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models.studentdb import Student

student = Blueprint('student', __name__)
student_model = Student()

@student.route('/')
def student_home():
    students = student_model.get_students_with_courses()
    return render_template("page-student.html", students = students)

@student.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        gender = request.form.get('gender')
        year = request.form.get('year')
        course_id = request.form.get('course')

        if not student_id or not first_name or not last_name or not gender or not year:
            flash('Name and code cannot be empty.', category='error')
        else:
            if not Student.is_student_unique(student_id, first_name, last_name, gender, year, course_id):
                flash('Student with the same id already exists', category='error')
            else:
                try:
                    student_query = Student(
                        student_id=student_id,
                        first_name=first_name,
                        last_name=last_name,
                        gender=gender,
                        year=year,
                        course_id=course_id
                    )
                    student_query.insert()
                    flash('Student added.', category='success')
                    return redirect(url_for('student.student_home'))
                except Exception as e:
                    flash('Student with the same id already exists', category='error')

    courses = Student.get_courses()

    return render_template("add-student.html", courses=courses)

@student.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        gender = request.form.get('gender')
        year = request.form.get('year')
        course_id = request.form.get('course')

        if not student_id or not first_name or not last_name or not gender or not year:
            flash('Name and code cannot be empty.', category='error')
        else:
            if not Student.is_student_unique(student_id, first_name, last_name, gender, year, course_id):
                flash('Student with the same id already exists.', category='error')
            else:
                try:
                    student_query = Student(id=id, student_id=student_id, first_name=first_name, last_name=last_name, gender=gender, year=year, course_id=course_id)
                    student_query.update()
                    flash('Student updated.', category='success')
                    return redirect(url_for('student.student_home'))
                except Exception as e:
                    flash('Student with the same id already exists', category='error')

    original_student = None
    students=Student.get_students_with_courses()
    for student in students:
        if student['id']== id:
            original_student = student
            break

    if original_student:
        courses = Student.get_courses()
        return render_template("edit-student.html", student=original_student, courses=courses)
    else:
        flash('Student not found.', category='error')
        return redirect(url_for('student.student_home'))
    

@student.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    student_query = Student(id=id)
    student_query.delete()
    flash('Student deleted.', category='success')
    return redirect(url_for('student.student_home'))

@student.route('/search', methods=['GET'])
def search_student():
    query = request.args.get('query')

    if not query:
        return redirect(url_for('student.student_home'))

    students = student_model.search_students(query)

    if not students:
        flash('No results found for the search query.', category='info')
