from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
plant_choices = (
    ('Indoor', "indoor"),
    ('Outdoor', 'outdoor'),
    ('Indoor/Outdoor', 'indoor/outdoor')
)

plant_style = (
    ('Full Plant', 'full plant'),
    ('Cutting', 'cutting'),
    ('Seed', 'seed')
)

class Plant(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250, default="This is a succulent")
    display_picture = models.FileField()
    plant_type = models.CharField(max_length = 30, choices=plant_choices, default='Indoor')
    plant_shape = models.CharField(max_length = 30, choices=plant_style, default='Cutting')
    uploader = models.ForeignKey(User,on_delete=models.CASCADE, related_name="plant_uploader")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title 
