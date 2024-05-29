import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from products.models import Product
from products.serializers import ProductSerializer
from .serializers import PredictionSerializer
from .utils import model
from rest_framework.permissions import AllowAny
from datetime import datetime, timedelta
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the API key
api_key = os.getenv('OPENAI_API_KEY')


client = OpenAI()

def check_if_holiday(date):
    # List of holiday dates
    holidays = [
        '2024-01-01', '2024-02-21', '2024-03-29', '2024-03-30', '2024-03-31', 
        '2024-04-01', '2024-04-18', '2024-05-01', '2024-05-25', '2024-08-12', 
        '2024-08-13', '2024-12-22', '2024-12-25', '2024-12-26'
    ]

    # Convert the list of strings to a list of datetime objects
    holidays = [datetime.strptime(holiday, '%Y-%m-%d') for holiday in holidays]

    # Check if the date is a holiday
    is_holiday = date in holidays

    return is_holiday

class PredictSales(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        serializer = PredictionSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            product_id = data['product_id']

            # Generate dates for the next 7 days
            dates = [datetime.now() + timedelta(days=i) for i in range(7)]

            predictions = []
            for date in dates:
                # Calculate day_of_week (0 = Monday, 6 = Sunday)
                day_of_week = date.weekday()

                # Check if the date is a holiday
                is_holiday = check_if_holiday(date)

                # Check if the date is in winter
                is_winter = 1 if date.month in [5, 6, 7] else 0

                # Check if the date is in summer
                is_summer = 1 if date.month in [12, 1, 2] else 0

                # One-hot encode the product ID
                product_id_data = pd.get_dummies(pd.Series([product_id]), prefix='product_id')

                # Ensure that the one-hot encoding always has 3 columns
                for i in range(1, 4):
                    column = f'product_id_{i}'
                    if column not in product_id_data:
                        product_id_data[column] = 0

                product_id_1 = product_id_data['product_id_1'].iloc[0]
                product_id_2 = product_id_data['product_id_2'].iloc[0]
                product_id_3 = product_id_data['product_id_3'].iloc[0]
                # Prepare the input for the model
                input_data = [
                    day_of_week, is_holiday, is_winter, is_summer,
                    product_id_1, product_id_2, product_id_3
                ]
                print("the input data is", input_data)
                # Make prediction
                prediction = model.predict([input_data])
                predictions.append({'date': date.strftime('%Y-%m-%d'), 'prediction': prediction[0]})

            return Response({'predictions': predictions}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProductInsights(APIView):
    permission_classes = [AllowAny]

    def get(self, request, product_id, format=None):
        # Get the product details
        product = Product.objects.get(id=product_id)
        serializer = ProductSerializer(product)
        product_data = serializer.data
        stock = product_data['items_remaining']
        print("items remaining", product_data['items_remaining'])
        # Generate dates for the next 7 days
        dates = [datetime.now() + timedelta(days=i) for i in range(7)]

        predictions = []
        for date in dates:
            # Calculate day_of_week (0 = Monday, 6 = Sunday)
            day_of_week = date.weekday()

            # Check if the date is a holiday
            is_holiday = check_if_holiday(date)

            # Check if the date is in winter
            is_winter = 1 if date.month in [5, 6, 7] else 0

            # Check if the date is in summer
            is_summer = 1 if date.month in [12, 1, 2] else 0

            # One-hot encode the product ID
            product_id_data = pd.get_dummies(pd.Series([product_id]), prefix='product_id')

            # Ensure that the one-hot encoding always has 3 columns
            for i in range(1, 4):
                column = f'product_id_{i}'
                if column not in product_id_data:
                    product_id_data[column] = 0

            product_id_1 = product_id_data['product_id_1'].iloc[0]
            product_id_2 = product_id_data['product_id_2'].iloc[0]
            product_id_3 = product_id_data['product_id_3'].iloc[0]
            # Prepare the input for the model
            input_data = [
                day_of_week, is_holiday, is_winter, is_summer,
                product_id_1, product_id_2, product_id_3
            ]
            print("the input data is", input_data)
            # Make prediction
            prediction = model.predict([input_data])
            predictions.append({'date': date.strftime('%Y-%m-%d'), 'prediction': prediction[0]})

        print("predictions made are", predictions)
        # Call the OpenAI completion endpoint
        OpenAI.api_key = api_key

        response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": 'You are a helpful assistant that helps informal traders in Bulawayo, Zimbabwe, with insights about the products they are selling. They want to know how to price and also stock based on the forecasted demand and the current stock they have. You are supposed to generate insights and give them back under the following format {"Price Suggestion": "You can price your bread slightly higher than usual due to the forecasted demand.","Stock Level": "","Stock Suggestion": "","More Insights": "".}. Your messages are supposed to be short and precise, remember this is for informal traders. the messages given above are just examples, you are supposed to come up with your own insights based on the data provied.'},
            {"role": "user", "content": f"I have {stock} units of {product.name} in stock. The demand for the next 7 days is predicted to be {', '.join([str(p['prediction']) for p in predictions])}. How should I price and stock my product?"}
        ]
        )
        # Format the response into a nice message
        # print(response.choices[0].message)
        insights_content = response.choices[0].message.content.strip()
        insights_list = insights_content.split('\n')
        insights_dict = json.loads(insights_list[0])

        return Response(data=insights_dict, status=status.HTTP_200_OK)
