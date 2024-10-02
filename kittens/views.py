from rest_framework import generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Breed, Kitten
from .serializers import BreedSerializer, KittenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth import login, authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny


# Получение списка пород
class BreedListView(generics.ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer


# Получение списка всех котят
class KittenListView(generics.ListAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer


# Получение котят определенной породы
class KittenByBreedView(generics.ListAPIView):
    serializer_class = KittenSerializer

    def get_queryset(self):
        breed_id = self.kwargs["breed_id"]
        return Kitten.objects.filter(breed_id=breed_id)


# Получение информации о котенке
class KittenDetailView(generics.RetrieveAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer


# Добавление информации о котенке
class KittenCreateView(generics.CreateAPIView):
    serializer_class = KittenSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Изменение информации о котенке
class KittenUpdateView(generics.UpdateAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if self.get_object().user != self.request.user:
            raise PermissionDenied("You can only update your own kittens.")
        serializer.save()


# Удаление информации о котенке
class KittenDeleteView(generics.DestroyAPIView):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own kittens.")
        instance.delete()


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "detail": "Logged in successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)

        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response(
                {"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Logged out successfully"}, status=status.HTTP_200_OK
        )
