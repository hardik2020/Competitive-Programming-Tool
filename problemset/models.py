from djongo import models

# Create your models here.
class Problems(models.Model):
    name = models.TextField()
    url = models.TextField()
    rating = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.url} {self.rating}"