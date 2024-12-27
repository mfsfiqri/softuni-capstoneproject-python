from django.core.exceptions import ValidationError
import re


def validate_no_special_characters(value):
    """
    Validate that the input contains only letters, numbers, and spaces
    """
    if not re.match(r'^[a-zA-Z0-9\s]+$', value):
        raise ValidationError(
            'Only letters, numbers, and spaces are allowed.',
            code='invalid_characters'
        )


def validate_word_count(value, min_words=10):
    """
    Validate minimum word count for content
    """
    words = value.split()
    if len(words) < min_words:
        raise ValidationError(
            f'Content must be at least {min_words} words long.',
            code='insufficient_words'
        )


def validate_unique_category_name(value):
    """
    Custom validator to ensure unique category names
    """
    from .models import Category
    if Category.objects.filter(name__iexact=value).exists():
        raise ValidationError(
            'A category with this name already exists.',
            params={'value': value}
        )