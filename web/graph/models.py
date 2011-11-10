from django.db import models

class Data(models.Model):
    time = models.DateTimeField()
    guest = models.CharField(max_length=32)
    measure = models.CharField(max_length=32)
    value = models.IntegerField()
