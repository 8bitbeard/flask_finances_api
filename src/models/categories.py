import enum
import uuid

from src.database import db


class CategoryType(enum.Enum):
    E = "Entrada"
    S = "Saída"


class Category(db.Model):
    __tablename__='categories'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    type = db.Column(db.Enum(CategoryType))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if not self.id:
            self.id = str(uuid.uuid4())

    def __repr__(self):
        return 'Category>>> {}'.format(self.id)
