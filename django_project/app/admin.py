from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Recipe, UserProfile, Tag

# Register your models here.
admin.site.register(Tag)