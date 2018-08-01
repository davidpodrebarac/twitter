from django.db import models
from twitter.users.models import User


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField("tag name", max_length=30, null=False, blank=False, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField("tweet message", max_length=200, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="creator of tweet",
        related_name="created_tweets",
        null=False,
    )
    tags = models.ManyToManyField(
        to=Tag,
        verbose_name='list of tags',
        related_name='associated_tweets',
    )

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.text[:20]
