import datetime
from django.db import models
from django.utils import timezone

class NewsArticle(models.Model):
    url = models.URLField(max_length=500)
    title = models.CharField(max_length=300)
    topic = models.CharField(max_length=100)
    synopsis = models.TextField()
    published_at = models.DateTimeField()
    
    def __str(self):
        return self.title