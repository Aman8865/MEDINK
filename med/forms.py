from django import forms
from .models import UserAccount

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = UserAccount
        fields = ['name', 'userid', 'password', 'usertype']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': ' ',
                'class': 'form-control'
            }),
            'userid': forms.TextInput(attrs={
                'placeholder': '',
                'class': 'form-control'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': '',
                'class': 'form-control'
            }),
            'usertype': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

class LoginForm(forms.Form):
    userid = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
