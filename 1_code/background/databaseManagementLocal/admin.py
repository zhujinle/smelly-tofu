from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import User, Menu, Order

admin.site.register(User)
admin.site.register(Menu)
admin.site.register(Order)