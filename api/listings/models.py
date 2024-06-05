from django.db import models

class Listing(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    price = models.CharField(max_length=100)
    facilities = models.TextField()
    address = models.TextField()
