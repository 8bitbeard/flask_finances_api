"""
User Schea File
"""

from src.database import ma

from src.models.users import User


class UserSchema(ma.SQLAlchemyAutoSchema):
    """
    User Schema Class
    """
    class Meta:
        """
        Meta Class
        """
        model = User
        load_instance = True
        fields = ("id", "name", "email")
        ordered = True
