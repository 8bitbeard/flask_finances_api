"""
Transaction Model File
"""

import uuid

from datetime import datetime

from src.database import db


class Transaction(db.Model):
    """
    Transaction Model Class
    """
    __tablename__ = 'transactions'

    id = db.Column(db.String(), primary_key=True)
    account_id = db.Column(db.String(), db.ForeignKey('accounts.id'), nullable=False)
    account = db.relationship('Account', backref='account', foreign_keys=[account_id])
    value = db.Column(db.Numeric(10, 2), nullable=True)
    category_id = db.Column(db.String(), db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', backref='category', foreign_keys=[category_id])
    created_at = db.Column(db.DateTime())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.id:
            self.id = str(uuid.uuid4())

        if not self.created_at:
            self.created_at = datetime.now()

    def __repr__(self):
        return 'Transaction>>> {}'.format(self.id)
