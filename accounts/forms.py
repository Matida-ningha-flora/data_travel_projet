from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    user_type = forms.ChoiceField(choices=User.USER_TYPE, initial='client')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'user_type', 'password1', 'password2']
