from django.contrib import admin

from accounts.models import Portfolio, PortfolioAsset, User

admin.site.register(User)
admin.site.register(Portfolio)
admin.site.register(PortfolioAsset)
