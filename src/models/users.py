"""
User Model File
"""

import uuid
from datetime import datetime

from src.database import db


class User(db.Model):
    """
    User Model Class
    """
    __tablename__ = 'users'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.now())
    updated_at = db.Column(db.DateTime(), onupdate=datetime.now())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.id:
            self.id = str(uuid.uuid4())

    def __repr__(self):
        return 'User>>> {}'.format(self.id)
