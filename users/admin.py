from django.contrib import admin

from users.models import *


class UserTypeAdmin(admin.ModelAdmin):
    list_display = ('username','phone_number')

# Register your models here.
admin.site.register(User, UserTypeAdmin)

