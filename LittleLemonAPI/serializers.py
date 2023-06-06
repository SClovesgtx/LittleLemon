from django.contrib.auth.models import User, Group
from rest_framework import serializers, permissions
from rest_framework.validators import UniqueValidator
import bleach

from .models import Category, MenuItem


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


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "groups"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
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
