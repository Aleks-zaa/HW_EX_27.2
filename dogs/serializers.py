# from rest_framework.fields import SerializerMethodField
# from rest_framework.serializers import ModelSerializer

from rest_framework import serializers

from dogs.models import Dog, Breed
from dogs.validators import validate_forbidden_words


class BreedSerializer(serializers.ModelSerializer):
    dogs = serializers.SerializerMethodField()

    def get_dogs(self, breed):
        return [dog.name for dog in Dog.objects.filter(breed=breed)]

    class Meta:
        model = Breed
        fields = "__all__"


class DogSerializer(serializers.ModelSerializer):
    breed = BreedSerializer(read_only=True)
    name = serializers.CharField(validators=[validate_forbidden_words])

    class Meta:
        model = Dog
        fields = "__all__"


class DogDetailSerializer(serializers.ModelSerializer):
    count_dog_with_same_breed = serializers.SerializerMethodField()
    breed = BreedSerializer()

    def get_count_dog_with_same_breed(self, dog):
        return Dog.objects.filter(breed=dog.breed).count()

    class Meta:
        model = Dog
        fields = ("name", "breed", "date_born", "count_dog_with_same_breed")
