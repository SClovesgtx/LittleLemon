from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import generics
from .models import Category, MenuItem, Cart
from .serializers import (
    CategorySerializer,
    MenuItemSerializer,
    ManagerSerializer,
    DeliveryCrewSerializer,
    CartManagementSerializer,
)
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import OnlyGETPermission, OnlyManagerPermission, OnlyClientPermission
from rest_framework.response import Response
from rest_framework import status


class CategoryView(generics.ListCreateAPIView):
    """
    Endpoint to list all categories and create new ones
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class MenuItemView(generics.ListCreateAPIView):
    """
    Endpoint to list all menu items and create new ones
    """

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyGETPermission]


class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update or delete a single menu item
    """

    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyGETPermission]


class ManagerView(generics.ListCreateAPIView):
    """
    View to list all managers and create new ones
    """

    queryset = User.objects.filter(groups__name="Manager")
    serializer_class = ManagerSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyManagerPermission]


class ManagerDeleteUserView(generics.DestroyAPIView):
    """
    Endpoint to delete managers users
    """

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
    Endpoint to list all delivery crew users and create new ones
    """

    queryset = User.objects.filter(groups__name="delivery crew")
    serializer_class = DeliveryCrewSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyManagerPermission]


class DeliveryCrewDeleteUserView(generics.DestroyAPIView):
    """
    Endpoint to delete delivery crew users
    """

    queryset = User.objects.filter(groups__name="delivery crew")
    serializer_class = DeliveryCrewSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyManagerPermission]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)


class CartManagementView(generics.ListCreateAPIView, generics.DestroyAPIView):
    """
    Endpoint to list all items in cart and create new ones
    """

    queryset = Cart.objects.all()
    serializer_class = CartManagementSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, OnlyClientPermission]

    def destroy(self, request, *args, **kwargs):
        user = request.user
        Cart.objects.filter(user=user).delete()
        return Response(status=status.HTTP_200_OK)
