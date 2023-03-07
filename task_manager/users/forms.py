from .models import LocalUser
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):

    class Meta:
        model = LocalUser
        fields = [
            'first_name',
            'last_name',
            'username',
            'password1',
            'password2'
        ]
