from django.db import models

# Create your models here.

class Contact(models.Model):
       name = models.CharField(max_length=200)
       email = models.EmailField()
       phone_number = models.CharField(max_length=20)
       query = models.TextField()

       class Meta:
        verbose_name_plural = "Contact Us"