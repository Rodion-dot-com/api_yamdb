from datetime import MINYEAR, datetime

from django.core.exceptions import ValidationError


def validate_year(value):
    if not MINYEAR <= value <= datetime.now().year:
        raise ValidationError('Год указан неправильно')
