from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_rest_paginate import Pagination
import logging
import sqlalchemy
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['JWT_ALGORITHM'] = os.getenv('JWT_ALGORITHM')
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
pagination = Pagination(app, db)

handler = logging.FileHandler('app.log')
handler.setLevel(logging.DEBUG)
logging.getLogger('sqlalchemy').addHandler(handler)

from .models import *
from .urls import *

from .config import db
db.create_all()
