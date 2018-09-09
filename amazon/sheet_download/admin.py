from django.contrib import admin

from .models import Orders, OrderItems, Inventory


admin.site.register(Orders)
admin.site.register(OrderItems)
admin.site.register(Inventory)
