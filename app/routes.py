from flask import Blueprint, render_template, url_for

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/debug')
def debug():
    return render_template('debug.html')