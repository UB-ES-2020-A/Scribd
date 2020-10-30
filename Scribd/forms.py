from django import forms

from Scribd.models import Ebook


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


'''
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    subscription = forms.ChoiceField(choices=["Free","Subscribed"])

    class Meta:
        model = Account
        fields = ["username","password1","password2","email","subscription"]

'''
