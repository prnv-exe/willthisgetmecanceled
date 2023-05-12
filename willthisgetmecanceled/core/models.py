from django.db import models

# Create your models here.

class Hate_Model(models.Model):
    text = models.CharField(max_length=200)
    hate = models.BooleanField()

    def __str__(self):
        return self.text
    
