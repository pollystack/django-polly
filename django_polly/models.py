from django.db import models


class Parrot(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Trick(models.Model):
    parrot = models.ForeignKey(Parrot, on_delete=models.CASCADE, related_name='tricks')
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ])
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} (performed by {self.parrot.name})"
