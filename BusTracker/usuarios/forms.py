from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm 
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm 
from django.contrib.auth import get_user_model


User = get_user_model()


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User  # Utiliza el modelo de usuario predeterminado de Django
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        if 'password' in self.fields:
            self.fields.pop('password')

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User  # Utiliza el modelo de usuario predeterminado de Django
        

