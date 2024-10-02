from django.contrib.auth.models import User
from django.db import models

class Breed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Kitten(models.Model):
    breed = models.ForeignKey(Breed, on_delete=models.CASCADE, related_name='kittens')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    description = models.TextField()

    def __str__(self):
        return f'{self.color} kitten, {self.age} months old'
