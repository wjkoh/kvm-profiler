from django.db import models

class Measurement(models.Model):
    time = models.DateTimeField()
    guest = models.CharField(max_length=256)
    measure = models.CharField(max_length=256)
    value = models.BigIntegerField()
