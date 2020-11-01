from datetime import datetime
from Scribd.models import Ebook
from Scribd.user_model import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms


class EbookForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = ['ebook_number', 'title', 'autor', 'description', 'is_promot', 'size', 'media_type', 'featured_photo',
                  'count_downloads']

        # TODO Gestionar featured_photo
        widgets = {
            'ebook_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'max lenght: 8 digits'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'max lenght: 50 characters'}),
            'autor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'max lenght: 50 characters'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_promot': forms.CheckboxInput(attrs={'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'class': 'form-control'}),
            'media_type': forms.Select(attrs={'class': 'form-control'}),
            'count_downloads': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    name = forms.TextInput()

    class Meta:
        model = User
        fields = ["username", "first_name", "password1", "password2", "email", "type"]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'max lenght: 20 digits'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'max lenght: 20 digits'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),

        }
