from djongo import models

# Create your models here.
class user(models.Model):
    username = models.TextField()
    password = models.TextField()