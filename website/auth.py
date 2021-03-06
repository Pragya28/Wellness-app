"""
    Provides the routes and functions related to user authentication
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash

from .models import User
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
        Allows a user to login to account
    """
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            flash('Incorrect password, try again', category='error')
        else:
            flash('Username does not exist.', category='error')
    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    """
        Allows a user to logout of the account
    """
    logout_user()
    return redirect(url_for('views.start'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    """
        Allows a new user to create account
    """
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))

    if request.method == 'POST':
        fullname = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        pwd1 = request.form.get('password1')
        pwd2 = request.form.get('password2')
        age = int(request.form.get('age'))
        gender = request.form.get('genderOptions')
        height = int(request.form.get('height'))
        weight = int(request.form.get('weight'))
        lifestyle = request.form.get('lifestyle')

        userbyusername = User.query.filter_by(username=username).first()
        userbyemail = User.query.filter_by(email=email).first()

        if userbyusername:
            message = "Username already exists"
            flash(message, category="error")
        elif userbyemail:
            message = "This email already has an account"
            flash(message, category="error")
        elif "." not in email.split("@")[-1]:
            message = "Invalid email address"
            flash(message, category="error")
        elif pwd1 != pwd2:
            message = "Unmatched passwords"
            flash(message, category="error")
        elif len(fullname.split()) < 2:
            message = "Please enter your full name"
            flash(message, category="error")
        elif age < 0:
            message = "Please enter valid age"
            flash(message, category="error")
        elif height < 0:
            message = "Please enter valid height"
            flash(message, category="error")
        elif weight < 0:
            message = "Please enter valid weight"
            flash(message, category="error")
        elif gender is None:
            message = "Select your gender"
            flash(message, category="error")
        elif lifestyle is None:
            message = "Select your lifestyle"
            flash(message, category="error")
        else:
            user = User(username, email, pwd1, fullname, gender, age, height, weight, lifestyle)
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            message = "Account created"
            flash(message, category="success")
            return redirect(url_for('views.home'))

    return render_template('signup.html', user=current_user)


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
        Allows a user to edit the profile details
    """
    if request.method == "POST" and request.form.get("save") == "save":
        fullname = request.form.get('name')
        age = int(request.form.get('age'))
        gender = request.form.get('genderOptions')
        height = float(request.form.get('height'))
        weight = float(request.form.get('weight'))
        lifestyle = request.form.get('lifestyle')

        if len(fullname.split()) < 2:
            message = "Please enter your full name"
            flash(message, category="error")
        elif age < 0:
            message = "Please enter valid age"
            flash(message, category="error")
        elif height < 0:
            message = "Please enter valid height"
            flash(message, category="error")
        elif weight < 0:
            message = "Please enter valid weight"
            flash(message, category="error")
        elif gender is None:
            message = "Select your gender"
            flash(message, category="error")
        elif lifestyle is None:
            message = "Select your lifestyle"
            flash(message, category="error")
        else:
            user_data = User.query.filter_by(id=current_user.id).first()
            user_data.update_profile(fullname, gender, age, height, weight, lifestyle)
            db.session.commit()
            message = "Your profile is updated"
            flash(message, category="success")
    return render_template("profile.html", user=current_user)
