from django.contrib.auth.base_user import BaseUserManager

from accounts.models import User

# mypy: ignore-errors


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):

        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.role = User.Role.ADMIN
        user.save()

        return user
