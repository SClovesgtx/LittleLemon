from django.contrib.auth.models import User, Group
from rest_framework import serializers, permissions
from rest_framework.validators import UniqueValidator
import bleach

from .models import Category, MenuItem, Cart, Order, OrderItem


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        required=True,
        max_length=50,
        validators=[UniqueValidator(queryset=Category.objects.all())],
    )

    class Meta:
        model = Category
        fields = "__all__"

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def validate_title(self, value):
        if len(value) <= 1:
            raise serializers.ValidationError(
                "Title must be at least 2 characters long"
            )
        return bleach.clean(value)


class MenuItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        required=True,
        max_length=50,
        validators=[UniqueValidator(queryset=MenuItem.objects.all())],
    )
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    featured = serializers.BooleanField()
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = "__all__"

    def create(self, validated_data):
        return MenuItem.objects.create(**validated_data)

    def validate_title(self, value):
        if len(value) <= 1:
            raise serializers.ValidationError(
                "Title must be at least 2 characters long"
            )
        return bleach.clean(value)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["groups"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """The user is created with manager group."""
        validated_data["is_staff"] = True
        validated_data["is_active"] = True
        user = User.objects.create_user(**validated_data)
        # get group manager
        group = Group.objects.get(name="Manager")
        user.groups.add(group)
        return user

    def update(self, instance, validated_data):
        # update user's password
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        return super().update(instance, validated_data)

    def validate_username(self, value):
        if len(value) <= 1:
            raise serializers.ValidationError(
                "Username must be at least 2 characters long"
            )
        return bleach.clean(value)

    def validate_email(self, value):
        if len(value) <= 1:
            raise serializers.ValidationError(
                "Email must be at least 2 characters long"
            )
        return bleach.clean(value)


class DeliveryCrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        validated_data["is_staff"] = True
        validated_data["is_active"] = True
        user = User.objects.create_user(**validated_data)
        group = Group.objects.get(name="delivery crew")
        user.groups.add(group)
        return user

    def update(self, instance, validated_data):
        # update user's password
        if "password" in validated_data:
            instance.set_password(validated_data["password"])
        return super().update(instance, validated_data)

    def validate_username(self, value):
        if len(value) <= 1:
            raise serializers.ValidationError(
                "Username must be at least 2 characters long"
            )
        return bleach.clean(value)

    def validate_email(self, value):
        if len(value) <= 1:
            raise serializers.ValidationError(
                "Email must be at least 2 characters long"
            )
        return bleach.clean(value)


class CartManagementSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(), read_only=True
    )
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    quantity = serializers.IntegerField(min_value=1)
    unit_price = serializers.DecimalField(
        max_digits=6, decimal_places=2, read_only=True
    )
    price = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)

    class Meta:
        model = Cart
        fields = ["user", "menuitem", "quantity", "unit_price", "price"]

    def to_internal_value(self, data):
        internal_value = super().to_internal_value(data)

        menu_item = internal_value["menuitem"]
        quantity = internal_value["quantity"]

        internal_value["unit_price"] = menu_item.price
        internal_value["price"] = menu_item.price * quantity

        return internal_value

    def create(self, validated_data):
        user = self.context["request"].user
        menu_item = validated_data["menuitem"]
        quantity = validated_data["quantity"]

        cart_item, created = Cart.objects.get_or_create(user=user, menuitem=menu_item)

        cart_item.quantity += quantity
        cart_item.unit_price = menu_item.price
        cart_item.price += menu_item.price * quantity

        cart_item.save()

        return cart_item


# class OrderSerializer(serializers.Serializer):
#     user = serializers.PrimaryKeyRelatedField(
#         default=serializers.CurrentUserDefault(), read_only=True
#     )
#     delivery_crew = serializers.PrimaryKeyRelatedField(
#         queryset=User.objects.filter(groups__name="delivery crew")
#     )
#     status = serializers.CharField(max_length=50, read_only=True)
#     total = serializers.DecimalField(max_digits=6, decimal_places=2, read_only=True)
#     date = serializers.DateTimeField(read_only=True)

#     class Meta:
#         model = Order
#         fields = ["user", "delivery_crew", "order_items", "status", "total", "date"]

#     def to_internal_value(self, data):
#         internal_value = super().to_internal_value(data)
#         user = self.context["request"].user
#         order_items = Cart.objects.filter(user=user).all()

#         total_price = 0
#         for order_item in order_items:
#             total_price += order_item.price

#         internal_value["total"] = total_price

#         return internal_value

#     def create(self, validated_data):
#         """
#         Creates a new order item for the current user.
#         Gets current cart items from the cart endpoints and
#         adds those items to the order items table.
#         Then deletes all items from the cart for this user.
#         """
#         user = self.context["request"].user
#         delivery_crew = validated_data["delivery_crew"]
#         # the most recent cart items witch has some items
#         cart = Cart.objects.filter(user=user).first()
#         order_items = [
#             MenuItem.objects.filter(title=item.menuitem.title) for item in cart
#         ]

#         order = Order.objects.create(
#             user=user, delivery_crew=delivery_crew, total=validated_data["total"]
#         )

#         for order_item in order_items:
#             OrderItem.objects.create(
#                 order=order,
#                 menuitem=order_item,
#                 quantity=cart.quantity,
#                 unit_price=order_item.unit_price,
#                 price=order_item.price,
#             )

#         Cart.objects.filter(user=user).delete()

#         return order
