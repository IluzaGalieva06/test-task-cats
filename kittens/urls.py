from django.urls import path
from .views import (
    BreedListView,
    KittenListView,
    KittenByBreedView,
    KittenDetailView,
    KittenCreateView,
    KittenUpdateView,
    KittenDeleteView
)

urlpatterns = [
    path('breeds/', BreedListView.as_view(), name='breed-list'),
    path('kittens/', KittenListView.as_view(), name='kitten-list'),
    path('kittens/breed/<int:breed_id>/', KittenByBreedView.as_view(), name='kittens-by-breed'),
    path('kittens/<int:pk>/', KittenDetailView.as_view(), name='kitten-detail'),
    path('kittens/create/', KittenCreateView.as_view(), name='kitten-create'),
    path('kittens/<int:pk>/update/', KittenUpdateView.as_view(), name='kitten-update'),
    path('kittens/<int:pk>/delete/', KittenDeleteView.as_view(), name='kitten-delete'),
]
