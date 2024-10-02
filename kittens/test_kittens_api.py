import pytest
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Breed, Kitten

User = get_user_model()


@pytest.fixture
def create_user():
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def create_breed():
    return Breed.objects.create(name="Persian")


@pytest.fixture
def create_kitten(create_breed, create_user):
    return Kitten.objects.create(
        breed=create_breed,
        user=create_user,
        color="White",
        age=2,
        description="Cute little kitten"
    )


@pytest.mark.django_db
def test_breed_list(client):
    Breed.objects.create(name="Siamese")

    response = client.get(reverse("breed-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Siamese"


@pytest.mark.django_db
def test_kitten_list(client, create_kitten):
    response = client.get(reverse("kitten-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["color"] == "White"


@pytest.mark.django_db
def test_kitten_by_breed(client, create_breed, create_kitten):
    response = client.get(reverse("kittens-by-breed", args=[create_breed.id]))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["color"] == "White"


@pytest.mark.django_db
def test_kitten_detail(client, create_kitten):
    response = client.get(reverse("kitten-detail", args=[create_kitten.id]))

    assert response.status_code == status.HTTP_200_OK
    assert response.data["color"] == "White"


@pytest.mark.django_db
def test_create_kitten(client, create_breed, create_user):
    client.login(username="testuser", password="testpass")

    data = {
        "breed": create_breed.id,
        "color": "Black",
        "age": 3,
        "description": "Playful kitten"
    }

    response = client.post(reverse("kitten-create"), data=data)

    assert response.status_code == status.HTTP_201_CREATED
    assert Kitten.objects.count() == 1
    assert Kitten.objects.last().color == "Black"


@pytest.mark.django_db
def test_update_kitten(client, create_breed, create_kitten):
    client.login(username="testuser", password="testpass")

    updated_data = {
        "breed": create_breed.id,
        "color": "Grey",
        "age": 3,
        "description": "Updated kitten description"
    }

    response = client.put(reverse("kitten-update", args=[create_kitten.id]),
                          data=updated_data,
                          content_type='application/json')

    assert response.status_code == status.HTTP_200_OK
    create_kitten.refresh_from_db()
    assert create_kitten.color == "Grey"
    assert create_kitten.age == 3
    assert create_kitten.description == "Updated kitten description"



@pytest.mark.django_db
def test_delete_kitten(client, create_kitten):
    client.login(username="testuser", password="testpass")

    response = client.delete(reverse("kitten-delete", args=[create_kitten.id]))

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Kitten.objects.count() == 0


@pytest.mark.django_db
def test_login(client):
    User.objects.create_user(username="testuser", password="testpass")

    data = {
        "username": "testuser",
        "password": "testpass"
    }

    response = client.post(reverse("login"), data=data)

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data


@pytest.mark.django_db
def test_logout(client, create_user):
    response = client.post(reverse("login"), {"username": "testuser", "password": "testpass"})
    refresh_token = response.data["refresh"]

    response = client.post(reverse("logout"), {"refresh": refresh_token})

    assert response.status_code == status.HTTP_200_OK
