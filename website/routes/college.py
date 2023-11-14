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
        college_name = request.form.get('college_name')
        college_code = request.form.get('college_code')

        if not college_name or not college_code:
            flash('Name and code cannot be empty.', category='error')
        else:
            if not College.is_college_unique(college_name, college_code):
                flash('College with the same name or code already exists.', category='error')
            else:
                college_query = College(college_name=college_name, college_code=college_code)
                college_query.insert()
                flash('College added.', category='success')
                return redirect(url_for('college.college_home'))

    return render_template('add-college.html')


@college.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_college(id):
    if request.method == 'POST':
        college_name=request.form.get('name')
        college_code=request.form.get('code')
        
        if not college_name or not college_code:
            flash('Name and code cannot be empty.', category='error')
        else:
            if not College.is_college_unique(college_name, college_code):
                flash('Course with the same name and code already exists for this college.', category='error')
            else:
                try:
                    college_query = College(id=id,college_name=college_name, college_code=college_code)
                    college_query.update()
                    flash('College updated.', category='success')
                    return redirect(url_for('college.college_home'))
                except Exception as e:
                    flash('College with the same name or code already exists.', category='error')

    original_college = None
    colleges = College.get_colleges()
    for college in colleges:
        if college['id'] == id:
            original_college = college
            break

    if original_college:
        return render_template("edit-college.html", college=original_college)
    else:
        flash('College not found.', category='error')
        return redirect(url_for('college.college_home'))


@college.route('/delete/<int:id>', methods=['POST'])
def delete_college(id):
    college_query = College(id=id)
    college_query.delete()
    flash('College deleted.', category='success')
    return redirect(url_for('college.college_home'))

@college.route('/search', methods=['GET'])
def search_colleges():
    query = request.args.get('query')

    if not query:
        return redirect(url_for('college.college_home'))
    colleges = college_model.search_colleges(query)

    if not colleges:
        flash('No results found for the search query.', category='info')

    return render_template('page-college.html', colleges=colleges)
