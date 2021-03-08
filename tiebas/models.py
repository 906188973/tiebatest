from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Topic(models.Model):
    """贴吧帖子主题"""
    text_topic = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    floor_many = models.IntegerField()

    def __str__(self):
        return self.text_topic

class poster(models.Model):
    """贴吧帖子"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    text_poster = models.TextField()
    floor = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'posters'

    def __str__(self):
        return self.text_poster[:50] + '...'

class Poster_reply(models.Model):
    """帖子回复"""
    poster = models.ForeignKey(poster, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

    by_owner = models.ForeignKey(User, null=True, related_name="replies", on_delete=models.SET_NULL)

    def __str__(self):
        return self.text[:50] + '...'