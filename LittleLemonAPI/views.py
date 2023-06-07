from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import generics
from .models import Category, MenuItem
from .serializers import (
    CategorySerializer,
    MenuItemSerializer,
    ManagerSerializer,
    DeliveryCrewSerializer,
)
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import OnlyGETPermission, OnlyManagerPermission


# Create your views here.
class CategoryView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyGETPermission]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyGETPermission]


class ManagerView(generics.ListCreateAPIView):
    """
    View to list all managers and create new ones
    """

    # get all Users from group manager
    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = ManagerSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyManagerPermission]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        group = Group.objects.get(name="Manager")
        context["default_groups"] = [group]
        return context


class DeliveryCrewView(generics.ListCreateAPIView):
    """
    View to list all managers and create new ones
    """

    # get all Users from group manager
    queryset = User.objects.filter(groups__name="delivery crew")
    serializer_class = DeliveryCrewSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyManagerPermission]
