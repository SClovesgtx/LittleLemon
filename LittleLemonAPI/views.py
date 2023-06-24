from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import generics
from .models import Category, MenuItem, Cart
from .serializers import (
    CategorySerializer,
    MenuItemSerializer,
    ManagerSerializer,
    DeliveryCrewSerializer,
    CartSerializer,
)
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    OnlyGETPermission,
    OnlyManagerPermission,
    OnlyCustomerPermission,
)
from rest_framework.response import Response
from rest_framework import status


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


class ManagerDeleteUserView(generics.DestroyAPIView):
    """
    View to list all managers and create new ones
    """

    # get all Users from group manager
    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = ManagerSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyManagerPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class DeliveryCrewView(generics.ListCreateAPIView):
    """
    View to list all managers and create new ones
    """

    # get all Users from group manager
    queryset = User.objects.filter(groups__name="delivery crew")
    serializer_class = DeliveryCrewSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyManagerPermission]


class DeliveryCrewDeleteUserView(generics.DestroyAPIView):
    """
    View to list all managers and create new ones
    """

    # get all Users from group manager
    queryset = User.objects.filter(groups__name="delivery crew")
    serializer_class = DeliveryCrewSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyManagerPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class CartView(generics.ListCreateAPIView, generics.DestroyAPIView):
    """
    View to list all managers and create new ones
    """

    # get all Users from group manager
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, OnlyCustomerPermission]
