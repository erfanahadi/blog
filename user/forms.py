from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Bloguser


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)
    image = forms.ImageField(required=False)

    class Meta:
        model = Bloguser
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'bio', 'image', 'phone_number')

    def clean(self):
        cleaned_data= super().clean()
        password1= cleaned_data.get('password1')
        password2= cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

class UserUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    class Meta:
        model = Bloguser
        fields = ('username', 'first_name', 'last_name', 'email', 'bio', 'image', 'phone_number')


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Bloguser
        fields = ('username', 'password')