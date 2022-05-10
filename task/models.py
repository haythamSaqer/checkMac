from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token


class Mac(models.Model):

    mac = models.CharField(max_length=200)
    vendor = models.CharField(max_length=200)

    def __str__(self):
        return self.mac

class Erorr(models.Model):

    erorr = models.CharField(max_length=200)

    def __str__(self):
        return self.erorr


class User(AbstractUser):
    CHOICES = [
        ('Basic', 'Basic'),
        ('Business', 'Business'),
        ('Agency', 'Agency'),
    ]

    first_name = models.CharField(max_length=200, null=True)
    username = models.CharField(unique=True, max_length=200)
    password = models.CharField(max_length=200)
    requestCounter = models.IntegerField(null=True)
    subscriptionPlan = models.CharField(choices=CHOICES, max_length=20, null=True)

    def __str__(self):
        return self.username


def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


post_save.connect(create_token, sender=User)

