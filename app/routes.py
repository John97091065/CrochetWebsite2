from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from .forms import RegisterForm
from .models import db, User

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/register' , methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Try logging in.', 'warning')
            return redirect(url_for('main.register'))

        hashed_password = generate_password_hash(form.password.data)

        new_user = User(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone_number.data,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('main.index'))

    return render_template('register.html', form=form)
