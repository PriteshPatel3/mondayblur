from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    #gives nested name space for configuration (keeps config in 1 place)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']