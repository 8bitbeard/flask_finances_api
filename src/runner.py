"""
Runner file for Heroku production
"""


import os

from src import create_app


application = create_app(os.environ['FLASK_ENV'])
