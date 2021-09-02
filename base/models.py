from django.db import models
from django.db.models.fields import IPAddressField
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.forms.models import ModelForm

class Box(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.GenericIPAddressField()
    version = models.CharField(max_length=200, blank=True)
    hostname = models.CharField(max_length=200, blank=True)
    up = models.BooleanField(default=False, blank=True)
    comments = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.ip

    class Meta:
        ordering = ['up']

class BoxService(models.Model):
    port = models.CharField(max_length=200, blank=True)
    extra = models.TextField(null=True, blank=True)
    cBox = models.ForeignKey(Box, on_delete=models.CASCADE)

    def __str__ (self):
        return self.port