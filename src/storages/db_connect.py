from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from src.settings import DBSettings

db = SQLAlchemy()
settings = DBSettings()


def init_db(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = settings.ps_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
