from django.db import models
from django.db.models.fields import IPAddressField
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.forms.models import ModelForm
from base.modules.notifications import Notification


class Box(models.Model):

    __original_ip = None
    __original_hostname = None
    __original_state = None

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    ip = models.GenericIPAddressField(null=False,blank=False)
    hostname = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    pwned = models.BooleanField(default=False)
    os = models.CharField(max_length=200, null=True, blank=True)
    new = models.BooleanField(default=True)
    updated = models.BooleanField(default=False)
    cidr = models.CharField(max_length=200, default="/24",null=True, blank=True)
    orderedip = models.BigIntegerField(null=True, blank=True, default=0)

    @property
    def get_ordered_ip(self):
        octets = self.ip.split(".")
        octet_num = (int(octets[0]) * 256^3) +  (int(octets[1]) * 256^2) + (int(octets[2]) * 256) + int(octets[3])
        return octet_num


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_ip = self.ip
        self.__original_hostname = self.hostname
        self.__original_state = self.state


    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        if (self.hostname != self.__original_hostname) or (self.state != self.__original_state):
            self.updated = True
        self.orderedip = self.get_ordered_ip
        self.__original_ip = self.ip
        self.__original_hostname = self.hostname
        self.__original_state = self.state
        super().save(force_insert, force_update, *args, **kwargs)



    def __str__(self):
        return self.ip

    class Meta:
        ordering = ['orderedip']

class BoxService(models.Model):

    __original_port = None
    __original_protocol = None
    __original_state = None
    __original_name = None
    __original_version = None
    __original_script = None
    
    port = models.IntegerField(blank=True)
    protocol = models.CharField(max_length=200, blank=True)
    state = models.TextField(null=True, blank=True)
    name = models.TextField(null=True, blank=True)
    version = models.TextField(null=True, blank=True)
    script = models.TextField(null=True,blank=True)
    new = models.BooleanField(default=True)
    updated = models.TextField(default=None,null=True, blank=True)
    #updated = models.BooleanField(default=False)
    cBox = models.ForeignKey(Box, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__original_port = self.port
        self.__original_protocol = self.protocol
        self.__original_state = self.state
        self.__original_name = self.name
        self.__original_version = self.version
        self.__original_script = self.script

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        temp = ""
        if self.protocol != self.__original_protocol:
            #n.append_notification(self.cBox, self.port, True, None, {"protocol":self.protocol})
            temp += "protocol: {}\n".format(self.protocol)
        if self.state != self.__original_state:
            temp += "state: {}\n".format(self.state)
        if self.name != self.__original_name:
            temp += "name: {}\n".format(self.name)
        if  self.version != self.__original_version:
            temp += "version: {}\n".format(self.version)
        if  self.script != self.__original_script:
            temp += "script: {}\n".format(self.script)
        if temp:
            self.updated = temp


        super().save(force_insert, force_update, *args, **kwargs)
        self.__original_port = self.port
        self.__original_protocol = self.protocol
        self.__original_state = self.state
        self.__original_name = self.name
        self.__original_version = self.version
        self.__original_script = self.script

    def __str__ (self):
        return str(self.port)

    class Meta:
        ordering=['port']