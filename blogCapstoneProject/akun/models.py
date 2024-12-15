from django.db import models
from django.contrib.auth.models import User
from blogCapstoneProject.akun.validations import validate_image_size

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)
    profile_pic = models.ImageField(
        upload_to='profile_pics',
        blank=True,
        validators=[validate_image_size]
    )
    def __str__(self):
        return self.user.username

