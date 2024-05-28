# predictions/serializers.py
from rest_framework import serializers

# class PredictionSerializer(serializers.Serializer):
#     day_of_week = serializers.IntegerField()
#     is_holiday = serializers.IntegerField()
#     is_winter = serializers.IntegerField()
#     is_summer = serializers.IntegerField()
#     product_id_1 = serializers.IntegerField()
#     product_id_2 = serializers.IntegerField()
#     product_id_3 = serializers.IntegerField()

class PredictionSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
