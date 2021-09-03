"""
Init Database File
"""

import locale

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
