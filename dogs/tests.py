from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from dogs.models import Breed, Dog
from users.models import User


class DogTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.breed = Breed.objects.create(name="Golden Retriever", description="Good dog")
        self.dog = Dog.objects.create(name="Max", breed=self.breed, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_dog_retrieve(self):
        url = reverse('dogs:dog-detail', args=(self.dog.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.dog.name)

    def test_dog_create(self):
        url = reverse('dogs:dog-list')
        data = {
            'name': 'Buddy'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dog.objects.all().count(), 2)

    def test_dog_update(self):
        url = reverse('dogs:dog-detail', args=(self.dog.pk,))
        data = {
            'name': 'Buddy'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Buddy')

    def test_dog_delete(self):
        url = reverse('dogs:dog-detail', args=(self.dog.pk,))
        response = self.client.delete(url)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dog.objects.all().count(), 0)

    def test_dog_list(self):
        url = reverse('dogs:dog-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.dog.pk,
                    'breed': {
                        'id': self.breed.pk,
                        'dogs': [
                            self.dog.name
                        ],
                        'name': self.breed.name,
                        'description': self.breed.description,
                        'owner': None
                    },
                    'name': self.dog.name,
                    'photo': None,
                    'date_born': None,
                    'owner': self.user.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class BreedTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@example.com")
        self.breed = Breed.objects.create(name="Golden Retriever", description="Good dog", owner=self.user)
        self.dog = Dog.objects.create(name="Max", breed=self.breed, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_breed_retrieve(self):
        url = reverse('dogs:breeds-retrieve', args=(self.breed.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), self.breed.name)

    def test_breed_create(self):
        url = reverse('dogs:breeds-create')
        data = {
            'name': 'Колли'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Breed.objects.all().count(), 2)

    def test_breed_update(self):
        url = reverse('dogs:breeds-update', args=(self.breed.pk,))
        data = {
            'name': 'Овчарка'
        }
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('name'), 'Овчарка')

    def test_breed_delete(self):
        url = reverse('dogs:breeds-delete', args=(self.breed.pk,))
        response = self.client.delete(url)
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Breed.objects.all().count(), 0)

    def test_breed_list(self):
        url = reverse('dogs:breeds-list')
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.breed.pk,
                    "dogs": [
                        self.dog.name
                    ],
                    "name": self.breed.name,
                    "description": self.breed.description,
                    "owner": self.user.pk
                }
            ]
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
