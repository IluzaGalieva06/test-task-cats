from rest_framework import serializers
from .models import Kitten, Breed

class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ['id', 'name']

class KittenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitten
        fields = ['id', 'breed', 'color', 'age', 'description', 'user']
        read_only_fields = ['user']
