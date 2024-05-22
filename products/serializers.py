from rest_framework import serializers
from .models import Product
from categories.serializers import CategorySerializer

class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200)
    description = serializers.CharField()
    category = CategorySerializer()

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category, _ = Category.objects.get_or_create(name=category_data['name'], defaults={'description': category_data['description']})
        product = Product.objects.create(category=category, **validated_data)
        return product

    def update(self, instance, validated_data):
        category_data = validated_data.pop('category')
        category, _ = Category.objects.get_or_create(name=category_data['name'], defaults={'description': category_data['description']})
        
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = category
        instance.save()
        return instance