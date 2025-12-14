from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_positive_price(value):
    if value <= 0:
        raise ValidationError(_('Цена должна быть больше 0.'))


def validate_no_bad_words(value):
    bad_words = {'дурак', 'скам'}  # пример, подставь свои
    lower = value.lower()
    for w in bad_words:
        if w in lower:
            raise ValidationError(_('Запрещённое слово в заголовке: %(word)s'), params={'word': w})


def validate_min_length_10(value):
    if len(value.strip()) < 10:
        raise ValidationError(_('Текст должен быть не короче 10 символов.'))


def validate_phone_simple(value):
    # Пример: разрешаем +, цифры, пробелы, дефисы
    allowed = set('+0123456789 -()')
    if any(ch not in allowed for ch in value):
        raise ValidationError(_('Телефон содержит недопустимые символы.'))
