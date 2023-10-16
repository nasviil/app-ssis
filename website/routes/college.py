from flask import Blueprint, render_template, request, flash

college = Blueprint('college', __name__)

@college.route('/')
def college_home():
    return render_template("college.html")

@college.route('/add', methods=['GET', 'POST'])
def add_college():
    if request.method =='POST':
        data = request.form
        print(data)
        flash('Student added.', category='success')

    return render_template("college-add.html")