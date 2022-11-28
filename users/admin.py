from django.contrib import admin
from .models import Profile, Posts, Followers, Comments


@admin.register(Posts)
class PostsTable(admin.ModelAdmin):
    list_display = ['blogger', 'title', 'posted']
    search_fields = ['title', 'blogger']


@admin.register(Profile)
class ProfilesTable(admin.ModelAdmin):
    list_display = ['name', 'gender', 'country']
    search_fields = ['name', 'country']

@admin.register(Followers)
class FollowersTable(admin.ModelAdmin):
    list_display = ['following', 'follower', 'followed',]

admin.site.register(Comments)