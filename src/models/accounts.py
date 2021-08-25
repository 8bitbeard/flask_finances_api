import uuid

from src.database import db


class Account(db.Model):
    __tablename__='accounts'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.String(), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='user', foreign_keys=[user_id])
    balance = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    income = db.Column(db.Numeric(10, 2), default=0, nullable=False)
    expense = db.Column(db.Numeric(10, 2), default=0, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.id:
            self.id = str(uuid.uuid4())

    def __repr__(self):
        return 'Account>>> {}'.format(self.id)
