from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SignUpForm(UserCreationForm):
    # username = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=254)

    # password1 = forms.PasswordInput()
    # password2 = forms.PasswordInput()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.PasswordInput()
