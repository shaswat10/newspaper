from django.db import models

# Create your models here.
class sourceModel(models.Model):
    id = models.SlugField(unique=True, primary_key=True)
    name = models.CharField(max_length=100)

class newsModel(models.Model):
    source = models.ForeignKey(sourceModel, on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    title = models.CharField(unique=True, max_length=1000)
    description = models.CharField(max_length=1000)
    url = models.URLField(max_length=200)
    urlToImage = models.URLField(max_length=1000)
    publishedAt = models.DateTimeField(null=True, blank=True)
    content = models.TextField()
