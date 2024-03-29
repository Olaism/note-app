from dataclasses import fields
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()

class CustomUserAdmin(UserAdmin):
    class Meta:
        add_form = CustomUserCreationForm
        form = CustomUserChangeForm
        model = CustomUser
        list_display = ('email', 'username')
        fields = ('email', 'username', 'first_name', 'last_name', 'profile_pic')

admin.site.register(CustomUser, CustomUserAdmin)


