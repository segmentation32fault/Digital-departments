from django.db import models

# Create your models here.


class User(models.Model):
    display_name = models.CharField(max_length=64)
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField()
    tags = models.ManyToManyField(Tag, related_name='posts')
