from django.db.models.signals import post_save #signal is post save
from django.contrib.auth.models import User #usermodel is gonna be sender who is sending a signal
from django.dispatch import receiver #receiver is going to sget this function
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs): #kwargs accepts any new arguments
    instance.profile.save()

