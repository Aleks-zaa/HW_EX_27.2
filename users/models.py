from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {"null": True, "blank": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="почта", help_text="укажите почту")
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name="телефон", help_text="укажите телефон")
    tg_nick = models.CharField(max_length=50, **NULLABLE, verbose_name="tg nick", help_text="укажите tg nick")
    avatar = models.ImageField(upload_to="users/avatars/", **NULLABLE, verbose_name="аватар",
                               help_text="загрузите аватар")
    tg_chat_id = models.CharField(max_length=50, **NULLABLE, verbose_name="Телеграм chat-id",
                                  help_text="Укажите телеграм chat-id")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class Donation(models.Model):
    amount = models.PositiveIntegerField(default=0, verbose_name="Сумма пожертвования", help_text="укажите сумму")
    session_id = models.CharField(max_length=250, **NULLABLE, verbose_name="id сессии", help_text="укажите id сессии")
    link = models.URLField(max_length=400, **NULLABLE, verbose_name="ссылка на оплату",
                           help_text="укажите ссылку на оплату")
    user_d = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Пользователь",
                               help_text="укажите пользователя", **NULLABLE)

    class Meta:
        verbose_name = "Пожертвование"
        verbose_name_plural = "Пожертвования"

    def __str__(self):
        return f"Пожертвование на сумму {self.amount}"
