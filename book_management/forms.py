from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms.widgets import PasswordInput

from .models import Comments



class UserCreateForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(required=True, widget=PasswordInput)


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comments
        exclude = ["book", "username"]