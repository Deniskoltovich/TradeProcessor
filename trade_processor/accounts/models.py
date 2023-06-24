from assets.models import Asset
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from mixins.models import EditCreationDateMixinModel

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


class User(AbstractUser, EditCreationDateMixinModel):
    class Role(models.TextChoices):
        ADMIN = "Admin"
        ANALYST = "Analyst"
        USER = "User"

    class Status(models.TextChoices):
        ACTIVE = "Active"
        INACTIVE = "Inactive"

    email = models.EmailField(unique=True, blank=False)
    role = models.CharField(
        choices=Role.choices, default=Role.USER, max_length=7
    )
    avatar_url = models.CharField(max_length=255, null=True, default=None)
    subscriptions = models.ManyToManyField(Asset, blank=True)
    status = models.CharField(
        choices=Status.choices, default=Status.INACTIVE, max_length=9
    )
    balance = models.DecimalField(
        max_digits=11, decimal_places=2, default=0.00
    )

    objects = UserManager()


class Portfolio(EditCreationDateMixinModel):
    user = models.ForeignKey(
        User, related_name="portfolios", on_delete=models.CASCADE
    )
    assets = models.ManyToManyField(Asset)
    name = models.CharField(max_length=64, default="My portfolio")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user}'s portfolio"
