from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AccountCreationForm(UserCreationForm):
    email = forms.CharField(max_length=254, widget=forms.EmailInput(), required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')