from django.conf import settings
from apps.accounts.models import User


class CreateData(object):
    def __init__(self) -> None:
        self.create_superuser()
        self.create_client()

    def create_superuser(self) -> User:
        # Create super user
        user_dict = {
            "first_name": "Test",
            "last_name": "Admin",
            "email": settings.FIRST_SUPERUSER_EMAIL,
            "password": settings.FIRST_SUPERUSER_PASSWORD,
            "is_superuser": True,
            "is_staff": True,
        }
        superuser = User.objects.get_or_none(email=user_dict["email"])
        if not superuser:
            superuser = User.objects.create_user(**user_dict)
        return superuser

    def create_client(self) -> User:
        # Create client
        user_dict = {
            "first_name": "Test",
            "last_name": "Client",
            "email": settings.FIRST_CLIENT_EMAIL,
            "password": settings.FIRST_CLIENT_PASSWORD,
        }
        user = User.objects.get_or_none(email=user_dict["email"])
        if not user:
            user = User.objects.create_user(**user_dict)
        return user
