from django.db import models
from django.db.models.fields import IPAddressField
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

class Box(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.GenericIPAddressField()
    version = models.CharField(max_length=200)
    hostname = models.CharField(max_length=200)
    up = models.BooleanField(default=False)
    comments = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.ip

    class Meta:
        ordering = ['up']


