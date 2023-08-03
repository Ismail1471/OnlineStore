from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'email', 'avatar', 'password1', 'password2']


