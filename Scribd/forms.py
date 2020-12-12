from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms
from django.contrib.auth.forms import UserCreationForm

from Scribd.models import *
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
            # 'featured_photo': forms.ImageField()
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['profile_image', 'portrait', 'bio']

        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_show_labels = False
        self.helper.layout = (Layout(
            Row(
                Column('profile_image', css_class='form-group col')
            ),
            Row(
                Column('portrait', css_class='form-group col')
            ),
            Row(
                Column('bio'),
            )))


class UpgradeAccountForm(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['subs_type']

        widget = {
            'subs_type': forms.Select(attrs={'class': 'form-control'})
        }

    helper = FormHelper()


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
            'file': forms.FileInput(attrs={'class': 'file-upload-input', 'onchange': 'readURL(this);'}),
            'visibility': forms.RadioSelect(choices=model.VISIBILITY_CHOICES)
        }


class UpdatePayment(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ["card_titular",
                  "card_number", "card_expiration",
                  "card_cvv"]


class RegisterForm(UserCreationForm):
    class Meta:
        model = User

        fields = ["username",
                  "first_name", "last_name",
                  "password1", "password2",
                  "email"]
        '''
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        '''


class Subscription(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ["subs_type", "card_titular",
                  "card_number", "card_expiration",
                  "card_cvv", ]

        widgets = {
            'card_titular': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Full name as displayed on the card'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'card_cvv': forms.PasswordInput(attrs={'class': 'form-control'}),
            'card_expiration': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'mm/yy'}),
        }


class CancelSubscription(forms.ModelForm):
    class Meta:
        model = userProfile
        fields = ['subs_type']


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
                attrs={'class': 'form-control'}),
            'ticket_summary': forms.Textarea(attrs={'class': 'form-control'}),
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["comment", "value_stars"]

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'})

        }


##################################
####### FORMS FORUM ##############
##################################


class CreateInForum(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ["topic", "description"]

        widgets = {
            'topic': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Forum title (cannot be left blank)'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CreateInDiscussion(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = "__all__"

        widgets = {
            'discuss': forms.Textarea(attrs={'class': 'form-control'}),
        }


class CreateInDiscussionTicket(forms.ModelForm):
    class Meta:
        model = DiscussionTickets
        fields = "__all__"

        widgets = {
            'discuss': forms.Textarea(attrs={'class': 'form-control'}),
        }
