from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from dogs.models import Dog
from dogs.services import send_telegram_message
from users.models import User


@shared_task
def send_information_about_like(email):
    message = 'Поставили лайк'
    send_mail('DRF', 'Поставили лайк', EMAIL_HOST_USER, [email])
    user = User.objects.get(email=email)
    if user.tg_chat_id:
        send_telegram_message(user.tg_chat_id, message)


@shared_task
def send_information_about_birthday():
    today = timezone.now().today()
    dogs = Dog.objects.filter(owner__isnull=False, date_born=today)
    email_list = []
    for dog in dogs:
        email_list.append(dog.owner.email)
    if email_list:
        send_mail('Поздравление', 'С днем рождения!', EMAIL_HOST_USER, email_list)
