from django.db import models
from django.contrib.auth.models import User
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
    RegexValidator
)
from .validators import (
    validate_no_special_characters,
    validate_word_count,
    validate_unique_category_name
)


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3, "Category name must be at least 3 characters long"),
            validate_no_special_characters,
            validate_unique_category_name
        ]
    )
    description = models.TextField(
        max_length=500,
        validators=[
            validate_word_count
        ]
    )

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, "Tag name must be at least 2 characters long"),
            RegexValidator(
                r'^[a-zA-Z0-9\s]+$',
                'Only letters, numbers, and spaces are allowed in tag names'
            )
        ]
    )

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(10, "Title must be at least 10 characters long"),
            MaxLengthValidator(100, "Title cannot exceed 100 characters")
        ]
    )
    content = models.TextField(
        validators=[
            validate_word_count  # Custom validator to ensure minimum content length
        ]
    )
    image = models.ImageField(upload_to='blog')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_tags(self):
        return ", ".join([tag.name for tag in self.tags.all()])

    def formatted_created_at(self):
        return self.created_at.strftime("%B %d, %Y")

    def formatted_updated_at(self):
        return self.updated_at.strftime("%B %d, %Y")


class Comment(models.Model):
    content = models.TextField(
        validators=[
            MaxLengthValidator(500, "Comment cannot exceed 500 characters")
        ]
    )
    blog = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}.{self.content[:20]}..."

    def formatted_created_at(self):
        return self.created_at.strftime("%B %d, %Y")