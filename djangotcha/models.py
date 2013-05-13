from django.db import models
from django.contrib.auth.models import User


class Person(models.Model):
    user = models.ForeignKey(User, unique=True)
    name = models.CharField(max_length=64)
    avatar_url = models.CharField(max_length=256)
    github_user_id = models.CharField(max_length=32)
    is_killed = models.BooleanField(default=False)
    date_killed = models.DateField(null=True)
    target = models.ForeignKey('self', null=True)
    secret_word = models.CharField(max_length=64)
    company = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        return "%s[%d]" % (self.name, self.id)
