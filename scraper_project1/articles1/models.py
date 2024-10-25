from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=100, null=True, blank=True)
    date_published = models.DateField(auto_now_add=True)
    content = models.TextField()
    url = models.URLField(max_length=500, unique=True)

    def __str__(self):
        return self.title

