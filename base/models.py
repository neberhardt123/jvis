from django.db import models
from django.db.models.fields import IPAddressField
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.forms.models import ModelForm

class Box(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.GenericIPAddressField()
    hostname = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    comments = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    pwned = models.BooleanField(default=False)
    os = models.CharField(max_length=200, blank=True)
    new = models.BooleanField(default=True)

    def __str__(self):
        return self.ip

    class Meta:
        ordering = ['ip']

class BoxService(models.Model):
    port = models.IntegerField(blank=True)
    protocol = models.CharField(max_length=200, blank=True)
    state = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    version = models.TextField(null=True, blank=True)
    script = models.TextField(null=True,blank=True)
    new = models.BooleanField(default=True)
    cBox = models.ForeignKey(Box, on_delete=models.CASCADE)

    def __str__ (self):
        return str(self.port)

    class Meta:
        ordering=['port']