"""
Category Model File
"""

import enum
import uuid

from src.database import db


class CategoryType(enum.Enum):
    """
    Category Type Enum
    """
    E = "Entrada"
    S = "Saída"


class Category(db.Model):
    """
    Category Model Class
    """
    __tablename__ = 'categories'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    type = db.Column(db.Enum(CategoryType))
    user_id = db.Column(db.String(), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='category_owner', foreign_keys=[user_id])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.id:
            self.id = str(uuid.uuid4())

    def __repr__(self):
        return 'Category>>> {}'.format(self.id)
