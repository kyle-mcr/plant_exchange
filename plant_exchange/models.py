from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.

class Plant(models.Model):
    title = models.CharField(max_length=50)
    plant_type = models.CharField(max_length = 30)
    plant_shape = models.CharField(max_length = 30)
    uploader = models.ForeignKey(User,on_delete=models.CASCADE, related_name="plant_uploader")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __repr__(self):
        return f"<Dojo object: {self.title}>"