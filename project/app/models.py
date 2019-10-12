from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Family(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    displayname = models.CharField(max_length=100, blank=True)
    family = models.ForeignKey(Family, related_name='user_family', on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    is_parent = models.BooleanField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.displayname


class GeoFence(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='geofence_user', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lat = models.CharField(max_length=50)
    long = models.CharField(max_length=50)
    radius = models.DecimalField(decimal_places=0, max_digits=3)
    is_active = models.BooleanField(default=True)


class History(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, related_name='history_user', on_delete=models.CASCADE)
    geofence = models.ForeignKey(GeoFence, related_name='history_geofence', on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_enter = models.BooleanField(null=True, blank=True)
    lat = models.CharField(max_length=50, null=True, blank=True)
    long = models.CharField(max_length=50, null=True, blank=True)
    is_emergency = models.BooleanField(null=True, blank=True)