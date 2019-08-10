from PIL import Image
from django.db import models
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField


TYPES = (
    ('company', 'company'),
    ('client', 'client'),
)


class User(AbstractUser):
    type = models.CharField(max_length=20, choices=TYPES)
    address = models.CharField(max_length=200, null=True)
    phone = PhoneField(blank=True, help_text='Contact phone number', null=True)

    def __str__(self):
        return self.type


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):

        return f'{self.user.username} Profile' #profile prople sanga nam ni dekhaucha

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  #run save method of parent class

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
