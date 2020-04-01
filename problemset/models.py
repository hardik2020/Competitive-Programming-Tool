from djongo import models

# Create your models here.
class Problems(models.Model):
    name = models.TextField()
    url = models.TextField()
    rating = models.DecimalField(max_digits=10,decimal_places=5)