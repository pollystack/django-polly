from django.db import models


class Parrot(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    tricks = models.TextField(blank=True)

    def __str__(self):
        return self.name
