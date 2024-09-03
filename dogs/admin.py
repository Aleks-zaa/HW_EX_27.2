from django.contrib import admin

from dogs.models import Dog, Breed

admin.site.register(Dog)
admin.site.register(Breed)