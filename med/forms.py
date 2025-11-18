from django import forms
from .models import UserAccount

# forms.py (replace or ensure this SignupForm exists)
from django import forms
from django.contrib.auth.hashers import make_password
from .models import UserAccount

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = UserAccount
        fields = ['name', 'userid', 'password', 'usertype']  # add contact if used
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'userid': forms.TextInput(attrs={'class': 'form-control'}),
            'usertype': forms.Select(attrs={'class': 'form-control'}),
            # 'contact': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        raw = self.cleaned_data.get('password')
        if raw:
            user.password = make_password(raw)
        if commit:
            user.save()
        return user


# class LoginForm(forms.Form):
#     userid = forms.CharField(max_length=50)
#     password = forms.CharField(widget=forms.PasswordInput)



from django import forms

class LoginForm(forms.Form):
    userid = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder':'User ID'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder':'Password'}))

