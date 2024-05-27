from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Product
from rest_framework.exceptions import ValidationError
from .serializers import ProductSerializer
from rest_framework.permissions import AllowAny
class ProductList(APIView):
    def get(self, request, format=None):
        products = Product.objects.filter(user=request.user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print("date", request.data)
        serializer = ProductSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            print("we are her")
            try:
                serializer.save()
            except ValidationError as e:
                return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"message": "An unexpected error occurred: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        errors = serializer.errors
        formatted_errors = {"message": " ".join([f"{field}: {str(err[0])}" for field, err in errors.items()])}
        return Response(data=formatted_errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView):
    def get_object(self, pk, user):
        try:
            return Product.objects.get(pk=pk, user=user)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk, request.user)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk, request.user)
        print("the data", request.data)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def patch(self, request, pk, format=None):
        product = self.get_object(pk, request.user)
        serializer = ProductSerializer(product, data=request.data, partial=True)  # set partial=True to update a data partially
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        print("haghaghg")
        product = self.get_object(pk, request.user)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    