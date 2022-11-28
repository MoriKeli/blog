from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    id = models.CharField(max_length=12, primary_key=True, editable=False)
    name = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    gender = models.CharField(max_length=7, blank=False)
    phone_no = models.CharField(max_length=14, blank=False)
    country = models.CharField(max_length=10, blank=False)
    dob = models.DateField(null=True, blank=False)
    age = models.PositiveIntegerField(default=0, editable=False)
    dp = models.ImageField(upload_to='Profile-pics/', default='default.png')
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        profile_pic = Image.open(self.dp.path)

        if profile_pic.height > 400 and profile_pic.width > 400:
            output_size = (400, 400)
            profile_pic.thumbnail(output_size)
            profile_pic.save(self.dp.path)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'User Profiles'


class Posts(models.Model):
    id = models.CharField(max_length=12, primary_key=True, editable=False)
    blogger = models.ForeignKey(Profile, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=60, blank=False)
    content = models.TextField(blank=False)
    posted = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.blogger}'

    class Meta:
        ordering = ['-posted']
        verbose_name_plural = 'Posts'


class Comments(models.Model):
    id = models.CharField(max_length=12, primary_key=True, editable=False)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, editable=False)
    name = models.ForeignKey(Profile, on_delete=models.CASCADE, editable=False)
    comment = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.post}'

    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Comments'


class Followers(models.Model):
    id = models.CharField(max_length=12, primary_key=True, editable=False, unique=True)
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, editable=False)
    follower = models.CharField(max_length=30, blank=False)
    followed = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.following}'


