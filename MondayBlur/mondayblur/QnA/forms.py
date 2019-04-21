from django import forms
from .models import comment
from django.contrib.auth.models import User

class CommentForm(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['comment','author']

