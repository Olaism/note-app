from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.CharField(max_length=254, widget=forms.EmailInput(), required=True)
    class Meta:
        model = get_user_model()
        fields = ('username', 'email',)

class CustomUserChangeForm(UserChangeForm):
    email = forms.CharField(max_length=254, widget=forms.EmailInput(), required=True)
    class Meta:
        model = get_user_model()
        fields = ('username', 'email',)