from django.contrib.auth.models import User
from django.db import models
from django.db.models import ManyToManyField


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(null=False, blank=True)

class Category(models.Model):
    name = models.CharField(max_length=40)

class Tag(models.Model):
    name = models.CharField(max_length=20)


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    tag = models.ManyToManyField(Tag, related_name="tag")
