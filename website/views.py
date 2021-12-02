from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from datetime import date
from .models import CalorieData, Data
from . import db
from .calculations import calculate_sleeping_time, calculate_calories_burned, total_calories

views = Blueprint('views', __name__)

SAVE_MSG = "Your data has been recorded"
UPDATE_MSG = "Your data has been updated"


@views.route('/', methods=['GET', 'POST'])
def start():
    if current_user.is_authenticated:
        return redirect(url_for("views.home"))
    if request.method == "POST":
        if request.form.get("login") == "login":
            return redirect(url_for('auth.login'))
        if request.form.get("signup") == "signup":
            return redirect(url_for('auth.signup'))
    return render_template("index.html", user=current_user)
    
@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route('/bmi')
@login_required
def bmi():
    bmi = current_user.bmi
    if bmi < 18.5:
        message = "You are underweight"
        category = "error"
    elif bmi < 24.9:
        message = "Your weight is normal"
        category = "success"
    elif bmi < 29.9:
        message = "You are overweight"
        category = "error"
    else:
        message = "You are obese"
        category = "error"
    flash(message, category=category)
    return render_template("bmi.html", user=current_user)

@views.route('/calorie', methods=["GET", "POST"])
@login_required
def calorie():
    old_data = CalorieData.query.filter_by(user_id=current_user.id, date=date.today())
    total = total_calories(old_data)
    if request.method == "POST":
        task = request.form.get("met-option")
        duration = int(request.form.get("duration"))
        if task in "":
            flash("Select activity - if desired activity is not available select the one which seems nearest", "error")
        else:
            met_val = float(task.split("-")[-1])
            cal = calculate_calories_burned(met_val, current_user.bmr, duration)
            task = task.replace("_"," ")[:task.index("-")]
            data = CalorieData(task, duration, cal)
            db.session.add(data)
            db.session.commit()
            flash(SAVE_MSG, category="success")
        
    return render_template("calorie.html", user=current_user, data=old_data, total=total)

@views.route('/sleep', methods=["GET", "POST"])
@login_required
def sleep():
    if request.method == "POST":
        sleep_time = request.form.get("sleep-time")
        wakeup_time = request.form.get("wakeup-time")
        duration = calculate_sleeping_time(sleep_time, wakeup_time)
        hrs = duration['hrs']
        mins = duration['mins']
        data = Data.query.filter_by(user_id=current_user.id, date=date.today()).first()
        if data:
            data.add_sleep(duration['total'])
            db.session.commit()
            flash(UPDATE_MSG, category="success")
        else:
            data = Data(current_user.id)
            data.add_sleep(duration['total'])
            db.session.add(data)
            db.session.commit()
            flash(SAVE_MSG, category="success")
    else:
        data = Data.query.filter_by(user_id=current_user.id, date=date.today()).first()
        if data:
            duration = data.sleep
            hrs = duration//60
            mins = duration%60
        else:
            hrs = 0
            mins = 0
            
    return render_template("sleep.html", user=current_user, hours=hrs, mins=mins)

@views.route('/water', methods=["GET", "POST"])
@login_required
def water():
    if request.method == "POST":
        amt = int(request.form.get("water"))/1000
        data = Data.query.filter_by(user_id=current_user.id, date=date.today()).first()
        if data:
            data.add_water(amt)
            db.session.commit()
            flash(UPDATE_MSG, category="success")
        else:
            data = Data(current_user.id)
            data.add_water(amt)
            db.session.add(data)
            db.session.commit()
            flash(SAVE_MSG, category="success")
    else:
        data = Data.query.filter_by(user_id=current_user.id, date=date.today()).first()
        if data:
            amt = data.water
        else:
            amt = 0
    return render_template("water.html", user=current_user, amt=amt)


@views.route('/nutrition', methods=["GET", "POST"])
@login_required
def nutrition():
    return render_template("nutrition.html", user=current_user)


@views.route('/activity', methods=["GET", "POST"])
@login_required
def activity():
    if request.method == "POST":
        text = request.form.get("activity").strip()
        stars = request.form.get("star")
        if stars:
            stars = int(stars)
        else:
            stars = 0
        data = Data.query.filter_by(user_id=current_user.id, date=date.today()).first()
        if data:
            data.add_activity(text, stars)
            db.session.commit()
            flash(UPDATE_MSG, category="success")
        else:
            data = Data(current_user.id)
            data.add_activity(text, stars)
            db.session.add(data)
            db.session.commit()
            flash(SAVE_MSG, category="success")
    else:
        data = Data.query.filter_by(user_id=current_user.id, date=date.today()).first()
        if data:
            text = data.activity
            stars = data.activity_rating
        else:
            text = ""
            stars = 0
    return render_template("activity.html", user=current_user, text=text, stars=stars)

@views.route('/learning', methods=["GET", "POST"])
@login_required
def learning():
    if request.method == "POST":
        text = request.form.get("learning").strip()
        stars = request.form.get("star")
        if stars:
            stars = int(stars)
        else:
            stars = 0
        data = Data.query.filter_by(user_id=current_user.id, date=date.today()).first()
        if data:
            data.add_learning(text, stars)
            db.session.commit()
            flash(UPDATE_MSG, category="success")
        else:
            data = Data(current_user.id)
            data.add_learning(text, stars)
            db.session.add(data)
            db.session.commit()
            flash(SAVE_MSG, category="success")
    else:
        data = Data.query.filter_by(user_id=current_user.id, date=date.today()).first()
        if data:
            text = data.learning
            stars = data.learning_rating
        else:
            text = ""
            stars = 0
    return render_template("learning.html", user=current_user, text=text, stars=stars)
    