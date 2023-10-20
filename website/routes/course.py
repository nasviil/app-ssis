from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models.coursedb import Course

course = Blueprint('course', __name__)
course_model = Course()

@course.route('/')
def course_home():
    courses = course_model.get_courses_with_college()
    return render_template("page-course.html", courses=courses)

@course.route('/add', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        college_id = request.form.get('college')

        if not name or not code:
            flash('Name and code cannot be empty.', category='error')
        else:
            if Course.is_unique(name, code, college_id):
                course_query = Course(
                    name=name,
                    code=code,
                    college_id=college_id
                )
                course_query.insert()
                flash('Course added.', category='success')
                return redirect(url_for('course.course_home'))
            else:
                flash('Course with the same name and code already exists for this college.', category='error')

    # Fetch the list of colleges from the database
    colleges = Course.get_colleges()

    return render_template("add-course.html", colleges=colleges)

@course.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_course(id):
    if request.method == 'POST':
        name = request.form.get('name')
        code = request.form.get('code')
        college_id = request.form.get('college')

        if not name or not code:
            flash('Name and code cannot be empty.', category='error')
        else:
            if Course.is_unique(name, code, college_id):
                # Update the existing course
                course_query = Course(id=id, name=name, code=code, college_id=college_id)
                course_query.update()
                flash('Course updated.', category='success')
                return redirect(url_for('course.course_home'))
            else:
                flash('Course with the same name and code already exists for this college.', category='error')

    original_course = None
    courses=Course.get_courses_with_college()
    for course in courses:
        if course['id']== id:
            original_course = course
            break

    if original_course:
        colleges = Course.get_colleges()
        return render_template("edit-course.html", course=original_course, colleges=colleges)
    else:
        flash('Course not found.', category='error')
        return redirect(url_for('course.course_home'))

@course.route('/delete/<int:id>', methods=['POST'])
def delete_course(id):
    course_query = Course(id=id)
    course_query.delete()
    flash('course deleted.', category='success')
    return redirect(url_for('course.course_home'))  # Redirect to the course home page
