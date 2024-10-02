from rest_framework import serializers
from .models import Kitten, Breed


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ["id", "name"]


class KittenSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    breed = serializers.PrimaryKeyRelatedField(queryset=Breed.objects.all())
    breed_name = serializers.CharField(source="breed.name", read_only=True)

    class Meta:
        model = Kitten
        fields = ["id", "breed", "breed_name", "color", "age", "description", "user"]
        read_only_fields = ["user"]
