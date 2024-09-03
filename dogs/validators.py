from rest_framework.serializers import ValidationError

forbidden_words = ['ставки', 'крипта']


def validate_forbidden_words(value):
    if value.lower() in forbidden_words:
        raise ValidationError('Содержание не должно содержать запрещенные слова.')
