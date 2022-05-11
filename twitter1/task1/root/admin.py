from django.contrib import admin
from django.contrib.auth import models
from .models import Profile, Tweet

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('id','user','post_text','post_image','post_date')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','dob','bio','location', 'profile_image')