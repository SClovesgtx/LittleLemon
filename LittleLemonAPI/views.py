from django.shortcuts import render
from rest_framework import generics
from .models import Category
from .serializers import CategorySerializer


# Create your views here.
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
