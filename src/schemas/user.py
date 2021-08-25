from src.database import ma

from src.models.users import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        fields = ("id", "name", "email")
        ordered = True