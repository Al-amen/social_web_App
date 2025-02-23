#account_app


from django.db import models
from django.contrib.auth.models import User
from newsfeed.models import Post

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True,default='profile_pictures/blank_profile.png')
    cover_picture = models.ImageField(upload_to='cover_pictures/', blank=True, null=True,default='cover_pictures/blank_cover.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.user.username} Profile'