from django.contrib.auth.base_user import BaseUserManager

from accounts.tasks.send_confirmation_email import (
    send_confirmation_email,
)

# mypy: ignore-errors


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):

        if email is None:
            raise TypeError("Users must have an email address.")

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        send_confirmation_email.delay(user.id)
        return user

    def create_superuser(self, email, password, **kwargs):

        if password is None:
            raise TypeError("Superusers must have a password.")

        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.role = user.Role.ADMIN
        user.save()

        return user
