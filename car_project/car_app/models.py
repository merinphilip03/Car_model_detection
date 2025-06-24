from django.db import models

class CarImages(models.Model):
    image = models.ImageField(upload_to='car/')
