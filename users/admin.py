from django.contrib import admin
from .models import Profile, Posts

admin.site.register(Profile)
@admin.register(Posts)
class PostsTable(admin.ModelAdmin):
    list_display = ['blogger', 'title', 'posted']
    search_fields = ['title', 'blogger']
    
