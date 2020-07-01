from django import forms
from .models import Plant


class PlantForm(forms.ModelForm):
    class Meta:
        model= Plant
        fields= ['title', 'display_picture', 'description', 'plant_type', 'plant_shape']
