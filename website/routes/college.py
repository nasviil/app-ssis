from flask import Blueprint, render_template, request, flash
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
