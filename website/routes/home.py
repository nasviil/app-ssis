from flask import Blueprint, render_template, flash

home = Blueprint('home', __name__)

@home.route('/')
def home_page():
    return render_template("homepage.html")