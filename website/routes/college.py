from flask import Blueprint, render_template, request, flash, redirect, url_for
from ..models.collegedb import College

college = Blueprint('college', __name__)
college_model = College()

@college.route('/')
def college_home():
    colleges = college_model.get_colleges()
    return render_template("page-college.html", colleges=colleges)

@college.route('/add', methods=['GET', 'POST'])
def add_college():
    if request.method == 'POST':
        college_query = College(
            name=request.form.get('name'),
            code=request.form.get('code')
        )
        college_query.insert()
        flash('College added.', category='success')
    return render_template("add-college.html")

@college.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_college(id):
    if request.method == 'POST':
        college_query = College(
            id=id,
            name=request.form.get('name'),
            code=request.form.get('code')
        )
        college_query.update()
        flash('College updated.', category='success')
        return redirect(url_for('college.college_home'))  # Redirect to the college home page

    college_data = college_model.get_colleges()
    return render_template("edit-college.html", college=college_data)