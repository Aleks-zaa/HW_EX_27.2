from django.db import models

from users.models import NULLABLE, User


class Breed(models.Model):
    name = models.CharField(max_length=100, verbose_name="порода", help_text="введите породу")
    description = models.TextField(**NULLABLE, verbose_name="описание", help_text="введите описание")
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец",
                              help_text="укажите владельца")

    class Meta:
        verbose_name = "порода"
        verbose_name_plural = "породы"


class Dog(models.Model):
    name = models.CharField(max_length=100, verbose_name="кличка", help_text="введите кличку")
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, verbose_name="порода", help_text="выберите породу",
                              **NULLABLE)
    photo = models.ImageField(upload_to="dogs/photo", verbose_name="photo", help_text="загрузите фото", **NULLABLE)
    date_born = models.DateField(verbose_name="дата рожденя", help_text="укажите дату рожденя", **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, **NULLABLE, verbose_name="Владелец",
                              help_text="укажите владельца")
    likes = models.ManyToManyField(User, verbose_name="Лайки", help_text="укажите лайки", **NULLABLE,
                                   related_name="user_likes")

    class Meta:
        verbose_name = "собака"
        verbose_name_plural = "собаки"
