from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tweet(models.Model):
    user = models.ForeignKey(User,to_field='id', on_delete=models.CASCADE)
    post_text = models.TextField(max_length=280,null=True, blank=True)
    post_image = models.ImageField(upload_to = '',null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=200, null=True, blank=True)
    location = models.TextField(max_length=30, null=True, blank=True)
    profile_image = models.ImageField(upload_to = 'profile_pics', null=True, blank=True)
    following = models.ManyToManyField(User, blank=True, related_name="following")
    