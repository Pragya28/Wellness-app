from . import db
from flask_login import UserMixin
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from .calculations import calculate_bmi, calculate_bmr
from flask_login import current_user

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    fullname = db.Column(db.String(150))
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    join_date = db.Column(db.Date)
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    lifestyle = db.Column(db.String(20))
    bmi = db.Column(db.Float)
    bmr = db.Column(db.Float)
    wellness = db.Column(db.Float, default=0.0)

    def __init__(self, username, email, password, fullname, gender, age, height, weight, lifestyle):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.fullname = fullname
        self.gender = gender 
        self.age = age
        self.height = height
        self.weight = weight
        self.lifestyle = lifestyle
        self.join_date = date.today()
        self.bmi = calculate_bmi(height, weight)
        self.bmr = calculate_bmr(height, weight, age, gender)


class CalorieData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date)
    exercise = db.Column(db.String(20))
    duration = db.Column(db.Integer)
    calorie = db.Column(db.Integer)

    def __init__(self, exercise, duration, calorie):
        self.user_id = current_user.id
        self.date = date.today()
        self.exercise = exercise
        self.duration = duration
        self.calorie = calorie


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date)
    calorie = db.Column(db.Float, default=0.0)
    sleep = db.Column(db.Integer, default=0)
    water = db.Column(db.Float, default=0.0)
    activity = db.Column(db.String(1000))
    activity_rating = db.Column(db.Integer,  default=0)
    learning = db.Column(db.String(1000))
    learning_rating = db.Column(db.Integer,  default=0)

    def __init__(self, user_id):
        self.user_id = user_id
        self.date = date.today()

    def add_calorie(self, calorie):
        self.calorie = calorie

    def add_sleep(self, sleep):
        self.sleep = sleep

    def add_water(self, water):
        self.water = water

    def add_activity(self, activity, activity_rating):
        self.activity = activity
        self.activity_rating = activity_rating

    def add_learning(self, learning, learning_rating):
        self.learning = learning
        self.learning_rating = learning_rating
