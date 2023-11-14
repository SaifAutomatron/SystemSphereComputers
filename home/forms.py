from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo, Items


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = '__all__'
        exclude = ('overall_rating', 'image_url',)

