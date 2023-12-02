from django import forms
from django.contrib.auth.models import User , Group
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
    
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta():
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'groups')