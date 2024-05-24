from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined')  # fields you want to display
    search_fields = ('username', 'email')  # fields you want to search by
    ordering = ('-date_joined',)  # order by date joined in descending order

admin.site.register(User, UserAdmin)