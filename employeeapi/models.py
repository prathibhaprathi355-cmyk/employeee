from django.db import models

# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=50)
    sal = models.IntegerField()
    branch = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
