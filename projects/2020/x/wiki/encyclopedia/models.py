from django.db import models


# Create your models here.
class Entry(models.Model):
    title = models.CharField(max_length=100)
    text = models.CharField(max_length=5000)
    
    def _str_(self):#changed to unicode, maybe this will fix the problem with data type
        return self.text

