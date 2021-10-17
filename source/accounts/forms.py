from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    def clean(self):
        cleaned_data = super().clean()
        # password = cleaned_data.get('password')
        # password_confirm = cleaned_data.get('password_confirm')
        # if password and password_confirm and password != password_confirm:
        #     raise forms.ValidationError('Passwords are not equal.')

    class Meta(UserCreationForm.Meta):
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']
