"""A simple flask web app"""
import os
import flask_login
from flask import Flask, render_template
from app.cli import create_database
from app.db import db
from app.auth import auth
from flask_wtf.csrf import CSRFProtect
from app.db.models import User
from flask_bootstrap import Bootstrap5
from app.simple_pages import simple_pages
from app.bank import bank
from app.logging_config import log_con
from app.context_processors import utility_text_processors
login_manager = flask_login.LoginManager()

def page_not_found(e):
    return render_template("404.html"), 404

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    if os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("app.config.ProductionConfig")
    elif os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("app.config.DevelopmentConfig")
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object("app.config.TestingConfig")
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    #app.secret_key = 'This is an INSECURE secret!! DO NOT use this in production!!'
    csrf = CSRFProtect(app)
    app.config['WTF_CSRF_ENABLED'] = False
    bootstrap = Bootstrap5(app)
    app.register_error_handler(404, page_not_found)
    app.context_processor(utility_text_processors)
    #db_dir = "database/db.sqlite"
    #app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'Lumen'
    #app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    #app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.register_blueprint(auth)
    app.register_blueprint(log_con)
    app.register_blueprint(simple_pages)
    app.register_blueprint(bank)
    # add command function to cli commands
    app.cli.add_command(create_database)
    db.init_app(app)

    return app

@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None
