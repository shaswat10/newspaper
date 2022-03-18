from django.db import models

# Create your models here.
class sourceModel(models.Model):
    source_id = models.SlugField(default=None, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class newsModel(models.Model):
    source = models.ForeignKey(sourceModel, on_delete=models.CASCADE)
    author = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(unique=True, max_length=1000)
    description = models.CharField(max_length=1000)
    url = models.URLField(max_length=200)
    urlToImage = models.URLField(max_length=1000)
    publishedAt = models.DateTimeField(null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.title