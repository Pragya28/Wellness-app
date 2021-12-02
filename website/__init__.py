from flask import Flask
from os import path, environ, remove, makedirs
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
import json

db = SQLAlchemy()
csrf = CSRFProtect()

def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is not None:
        app.config.from_file(test_config, load=json.load)
        db_name = app.config["DB_NAME"]
    else:
        app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
        db_name = environ.get('DB_NAME')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_name}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    csrf.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Data, CalorieData
    create_database(app, db_name)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app, db_name):
    if not path.exists('website/'+db_name):
        db.create_all(app=app)
        print("Database created")
