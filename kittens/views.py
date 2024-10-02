from rest_framework import generics, permissions
from .models import Breed, Kitten
from .serializers import BreedSerializer, KittenSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

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
        breed_id = self.kwargs['breed_id']
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
