from django import forms
from django.contrib.auth.forms import UserCreationForm

from Scribd.models import Ebook, UserTickets, UploadedResources
from .user_models import User, userProfile


class EbookForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = ['ebook_number', 'title', 'autor', 'description', 'size', 'media_type', 'featured_photo']

        widgets = {
            'ebook_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'max lenght: 8 digits'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'autor': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'size': forms.NumberInput(attrs={'class': 'form-control'}),
            'media_type': forms.Select(attrs={'class': 'form-control'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['bio']

        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'})
        }


class UpgradeAccountForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['subs_type']


class FollowForm(forms.ModelForm):
    class Meta:
        model = Ebook
        fields = ['follower']


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedResources
        fields = ['title', 'visibility', 'file', 'featured_photo']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'visibility': forms.RadioSelect(choices=model.VISIBILITY_CHOICES)
        }


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username",
                  "first_name", "last_name",
                  "password1", "password2",
                  "email"]

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


"""
class CreditCardForm(forms.ModelForm):
    class Meta:
        model = SubscribedUsers
        fields = ['username', "card_titular",
                  "card_number", "card_expiration",
                  "card_cvv", ]

        # TODO Gestionar featured_photo
        widgets = {
            'card_titular': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Full name as displayed on the card'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'card_cvv': forms.PasswordInput(attrs={'class': 'form-control'}),
            'card_expiration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mm/yy'}),
        }
"""


class Subscription(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ["subs_type", "card_titular",
                  "card_number", "card_expiration",
                  "card_cvv", ]

        # TODO Gestionar featured_photo
        widgets = {
            'card_titular': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Full name as displayed on the card'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'card_cvv': forms.PasswordInput(attrs={'class': 'form-control'}),
            'card_expiration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mm/yy'}),
        }


class ProfileFormProvider(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class TicketForm(forms.ModelForm):
    class Meta:
        model = UserTickets
        fields = ["ticket_title", "ticket_summary"]

        widgets = {
            'ticket_title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ticket title (cannot be left blank)'}),
            'ticket_summary': forms.Textarea(attrs={'class': 'form-control'}),
        }
