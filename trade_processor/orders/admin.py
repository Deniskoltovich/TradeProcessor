from django.contrib import admin

from orders.models import AutoOrder, Order

admin.site.register(Order)
admin.site.register(AutoOrder)
