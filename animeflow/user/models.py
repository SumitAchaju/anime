from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from helpers.cloudinary.upload_presets import profile_image


class User(AbstractUser):
    profile = CloudinaryField("image", **profile_image)

    def __str__(self):
        return self.username
