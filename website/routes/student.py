from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models.studentdb import Student
import cloudinary
import cloudinary.uploader
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg'}
MAX_FILE_SIZE = 1 * 1024 * 1024

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

student = Blueprint('student', __name__)
student_model = Student()

@student.route('/')
def student_home():
    students = student_model.get_students_with_courses()
    return render_template("page-student.html", students = students)

@student.route('/add', methods=['GET', 'POST'])
def add_student():
    print(request.method)
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
                    if 'student_photo' in request.files:
                        uploaded_file = request.files['student_photo']
                        if uploaded_file and allowed_file(uploaded_file.filename):
                            if uploaded_file.content_length > MAX_FILE_SIZE:
                                flash('File size exceeds the limit of 1MB. Please choose a smaller file.', category='error')
                                return redirect(url_for('student.add_student'))
                            cloudinary_response = cloudinary.uploader.upload(uploaded_file)
                            cloudinary_url = cloudinary_response.get('secure_url', '')

                            student_query = Student(
                                student_id=student_id,
                                first_name=first_name,
                                last_name=last_name,
                                gender=gender,
                                year=year,
                                course_id=course_id,
                                cloudinary_url=cloudinary_url
                            )
                            student_query.insert()
                            flash('Student added.', category='success')
                            return redirect(url_for('student.student_home'))
                        else:
                            flash('Error uploading student. Invalid file format. Use jpg or png.', category='error')
                            return redirect(url_for('student.add_student'))

                except Exception as e:
                    print(f"Error adding student: {e}")
                    flash('Error adding student. Please try again.', category='error')

    courses = Student.get_courses()

    return render_template("add-student.html", courses=courses)
    #rubber ducky

@student.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        #nice
        gender = request.form.get('gender')
        year = request.form.get('year')
        course_id = request.form.get('course')

        if not student_id or not first_name or not last_name or not gender or not year:
            flash('Name and code cannot be empty.', category='error')
        else:
            if not Student.is_student_unique(student_id, first_name, last_name, gender, year, course_id, current_student_id=id):
                flash('Student with the same id already exists.', category='error')
            else:
                try:
                    if 'student_photo' in request.files:
                        uploaded_file = request.files['student_photo']
                        if uploaded_file:
                            cloudinary_response = cloudinary.uploader.upload(uploaded_file)
                            cloudinary_url = cloudinary_response.get('secure_url', '')
                        else:
                            cloudinary_url = original_student['cloudinary_url']

                    student_query = Student(
                        id=id,
                        student_id=student_id,
                        first_name=first_name,
                        last_name=last_name,
                        gender=gender,
                        year=year,
                        course_id=course_id,
                        cloudinary_url=cloudinary_url
                    )
                    student_query.update()
                    flash('Student updated.', category='success')
                    return redirect(url_for('student.student_home'))
                except Exception as e:
                    flash('Error updating student.', category='error')

    original_student = None
    students = Student.get_students_with_courses()
    for student in students:
        if student['id'] == id:
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
    print(students)

    if not students:
        flash('No results found for the search query.', category='info')

    return render_template('page-student.html', students=students)

