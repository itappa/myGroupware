from django.db import models
from django.conf import settings

class Feed(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Entry(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=200)
    link = models.URLField()
    description = models.TextField()
    published_date = models.DateTimeField()
    author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-published_date']
        verbose_name_plural = 'entries'

class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='subscriptions')
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'feed')

class ReadStatus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'entry')