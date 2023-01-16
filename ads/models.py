from django.db import models


class Advertisement(models.Model):
    name = models.CharField(max_length=150)
    author = models.CharField(max_length=50)
    price = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.CharField(max_length=500)
    address = models.CharField(max_length=150)
    is_published = models.BooleanField(default=False)


class Category(models.Model):
    name = models.CharField(max_length=100)
