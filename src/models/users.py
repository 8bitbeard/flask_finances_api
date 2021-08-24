import uuid

from src.database import db


class User(db.Model):
    __tablename__='users'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.id:
            self.id = str(uuid.uuid4())

    def __repr__(self):
        return 'User>>> {}'.format(self.id)