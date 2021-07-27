from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Pose(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    angle1 = models.CharField(max_length=64)
    angle2 = models.CharField(max_length=64)
    angle3 = models.CharField(max_length=64)
    angle4 = models.CharField(max_length=64)
    angle5 = models.CharField(max_length=64)
    angle6 = models.CharField(max_length=64)


class Choice(models.Model):
    name = models.CharField(max_length=64)
    number = models.IntegerField()
