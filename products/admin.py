from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category','items_remaining','items_sold','user')  
    search_fields = ('name', 'category__name')
    ordering = ('name',) 

admin.site.register(Product, ProductAdmin)