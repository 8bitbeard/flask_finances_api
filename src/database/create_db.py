"""
Script to create the DB on Heroku
"""


import os

from src.database import db
from src import create_app

db.create_all(app=create_app(os.environ['FLASK_ENV']))
