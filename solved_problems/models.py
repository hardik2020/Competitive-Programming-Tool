from djongo import models

# Create your models here.
class Solved_Probelms(models.Model):
    username = models.TextField()
    name = models.TextField()

    def __str__(self):
        return f"{self.username} {self.name}"

# {% url 'load' list_u1.0 %}