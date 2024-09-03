from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView, ListAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from dogs.models import Dog, Breed
from dogs.paginations import CustomPagination
from dogs.serializers import DogSerializer, BreedSerializer, DogDetailSerializer
from dogs.tasks import send_information_about_like
from users.permissions import IsModer, IsOwner


class DogViewSet(ModelViewSet):
    queryset = Dog.objects.all()
    # serializer_class = DogSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ('breed',)
    ordering_fields = ('date_born',)
    search_fields = ('name',)
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DogDetailSerializer
        return DogSerializer

    def perform_create(self, serializer):
        dog = serializer.save()
        dog.owner = self.request.user
        dog.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (IsOwner,) #~IsModer,
        return super().get_permissions()

    @action(detail=True, methods=('post',))
    def likes(self, request, pk):
        dog = get_object_or_404(Dog, pk=pk)
        if dog.likes.filter(pk=request.user.pk).exists():
            dog.likes.remove(request.user)
        else:
            dog.likes.add(request.user)
            send_information_about_like.delay(dog.owner.email)
        serializer = self.get_serializer(dog)
        return Response(data=serializer.data)



class BreedCreateAPIView(CreateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsAuthenticated, ~IsModer,)

    def perform_create(self, serializer):
        breed = serializer.save()
        breed.owner = self.request.user
        breed.save()


class BreedListAPIView(ListAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    pagination_class = CustomPagination


class BreedUpdateAPIView(UpdateAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class BreedRetrieveAPIView(RetrieveAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class BreedDestroyAPIView(DestroyAPIView):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    permission_classes = (IsAuthenticated, ~IsModer | IsOwner)
