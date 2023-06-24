from django.contrib.auth.models import User, Group
from rest_framework import serializers, permissions
from rest_framework.validators import UniqueValidator
import bleach

from .models import Category, MenuItem, Cart


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


class CartSerializer(serializers.Serializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    menuitem = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        model = Cart
        fields = "__all__"
        extra_kwargs = {
            "quantity": {"min": 1},
            "unit_price": {"min": 0.01},
            "price": {"min": 0.01},
        }

    def create(self, validated_data):
        # get menu-item price
        # menu_item = MenuItem.objects.get(id=validated_data["menuitem"])
        # validated_data["unit_price"] = menu_item.price
        # validated_data["price"] = menu_item.price * validated_data["quantity"]
        # # get User by name from User model
        # user = User.objects.get(username=validated_data["user"])
        # validated_data["user"] = user
        return super().create(validated_data)
