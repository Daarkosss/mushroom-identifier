import os
from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = 'src/web_app/static/images/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SECRET_KEY'] = 'tajny-klucz'

    db.init_app(app)
    Migrate(app, db)
    return app


db = SQLAlchemy()

app = create_app()
login_manager = LoginManager(app)
login_manager.login_view = 'login'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
