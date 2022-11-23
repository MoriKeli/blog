from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Posts, Comments
from datetime import datetime
import uuid


@receiver(pre_save, sender=Profile)
def generate_ProfileId(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:12]

    try:
        if datetime.now().strftime('%Y-%m-%d %H:%M:%S') > instance.created.strftime('%Y-%m-%d %H:%M:%S'):
            user_dob = str(instance.dob)
            get_userDob = datetime.strptime(user_dob, '%Y-%m-%d')
            current_date = datetime.now()
            user_age = current_date - get_userDob
            convert_usersAge = int(user_age.days/365.25)
            instance.age = convert_usersAge
            
        else:
            user_dob = str(instance.dob)
            get_VoterDob = datetime.strptime(user_dob, '%Y-%m-%d')
            current_date = datetime.now()
            user_age = current_date - get_userDob
            convert_usersAge = int(user_age.days/365.25)
            instance.age = convert_usersAge
    
    except AttributeError:
        return


@receiver(pre_save, sender=Posts)
def generate_BlogId(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:12]

@receiver(pre_save, sender=Comments)
def generate_commentsId(sender, instance, **kwargs):
    if instance.id == "":
        instance.id = str(uuid.uuid4()).replace('-', '')[:12]


@receiver(post_save, sender=User)
def save_userprofile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff is False and instance.is_superuser is False:
            Profile.objects.create(name=instance)

