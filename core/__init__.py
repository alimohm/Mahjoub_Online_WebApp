from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # جلب الرابط من المتغيرات التي وضعناها في رويال
    database_url = os.environ.get('DATABASE_URL')

    # تصحيح الرابط إذا كان يبدأ بـ postgres:// (ضروري لـ SQLAlchemy 3+)
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app
