from flask import Blueprint, render_template, url_for, request, render_template_string
import bcrypt

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/debug')
def debug():
    return render_template('debug.html')

@main.route('/register')
def register():
    return render_template('register.html')

# @main.route('/login')
# def login():
#     return render_template('login.html')

# @main.route('/logout')
# def logout():
#     return render_template('logout.html')