from django.urls import path
from rest_framework.routers import SimpleRouter
from dogs.views import (DogViewSet, BreedCreateAPIView, BreedListAPIView, BreedUpdateAPIView, BreedRetrieveAPIView,
                        BreedDestroyAPIView)
from dogs.apps import DogsConfig

app_name = DogsConfig.name

router = SimpleRouter()
router.register("", DogViewSet)

urlpatterns = [
    path("breeds/", BreedListAPIView.as_view(), name="breeds-list"),
    path("breeds/<int:pk>/", BreedRetrieveAPIView.as_view(), name="breeds-retrieve"),
    path("breeds/create/", BreedCreateAPIView.as_view(), name="breeds-create"),
    path("breeds/<int:pk>/delete/", BreedDestroyAPIView.as_view(), name="breeds-delete"),
    path("breeds/<int:pk>/update/", BreedUpdateAPIView.as_view(), name="breeds-update")

]

urlpatterns += router.urls
