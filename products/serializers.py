from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Product
from  categories.models import Category
from categories.serializers import CategorySerializer
from django.core.exceptions import ValidationError

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    category = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
    items_remaining = serializers.IntegerField()
    items_sold = serializers.IntegerField(default=0)



    def create(self, validated_data):
        category_id = validated_data.pop('category')
        category = get_object_or_404(Category, id=category_id)
        user = self.context['request'].user
        product = Product.objects.create(category=category, user=user, **validated_data)
        return product

    def update(self, instance, validated_data):
        category_id = validated_data.pop('category')
        category = get_object_or_404(Category, id=category_id)
        
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.description)
        instance.items_remaining = validated_data.get('items_remaining', instance.description)
        instance.items_sold = validated_data.get('items_sold', instance.description)
        instance.category = category
        instance.save()
        return instance