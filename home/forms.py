from django import forms
from django.contrib.auth.models import User
from .models import Items, Customer
from django.contrib.auth.forms import UserCreationForm


class ItemsForm(forms.ModelForm):
    class Meta:
        model = Items
        fields = '__all__'
        exclude = ('overall_rating',)
        widgets = {
          'image_url': forms.HiddenInput(),
         }


class UserSignupForm(UserCreationForm):

    class Meta():
        model = User
        fields = ('username', 'email')