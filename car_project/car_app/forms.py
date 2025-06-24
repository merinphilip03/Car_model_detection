from django import forms
from .models import CarImages


class CarImageForm(forms.ModelForm):

    class Meta:
        model = CarImages
        fields = ['image']