from datetime import datetime, MINYEAR

from django.core.exceptions import ValidationError


def validate_year(value):
    if value < MINYEAR or value > datetime.now().year:
        raise ValidationError('Год указан неправильно')