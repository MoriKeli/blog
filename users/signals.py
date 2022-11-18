from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Posts
import uuid


@receiver(pre_save, sender=Profile)
def generate_ProfileId(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:12]

@receiver(pre_save, sender=Posts)
def generate_BlogId(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:12]


@receiver(post_save, sender=User)
def save_userprofile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff is False and instance.is_superuser is False:
            Profile.objects.create(name=instance)
