from django.urls import path
from . import views

urlpatterns = [
    path("categories/", views.CategoryView.as_view()),
    path("menu-items/", views.MenuItemView.as_view()),
    path("menu-items/<int:pk>/", views.SingleMenuItemView.as_view()),
    path("groups/manager/users/", views.ManagerView.as_view()),
    path("groups/manager/users/<int:pk>", views.ManagerDeleteUserView.as_view()),
    path("groups/delivery-crew/users/", views.DeliveryCrewView.as_view()),
    path(
        "groups/delivery-crew/users/<int:pk>",
        views.DeliveryCrewDeleteUserView.as_view(),
    ),
    path("cart/menu-items", views.CartManagementView.as_view()),
]
