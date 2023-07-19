from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Portfolio, User

admin.site.register(User)
admin.site.register(Portfolio)
