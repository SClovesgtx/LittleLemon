from rest_framework import serializers
from rest_framework.validators import UniqueValidator
import bleach

from .models import Category


class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        required=True,
        max_length=50,
        validators=[UniqueValidator(queryset=Category.objects.all())],
    )

    def create(self, validated_data):
        return Category.objects.create(**validated_data)

    def validate_title(self, value):
        if len(value) <= 1:
            raise serializers.ValidationError(
                "Title must be at least 2 characters long"
            )
        return bleach.clean(value)