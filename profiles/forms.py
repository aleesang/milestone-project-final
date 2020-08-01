from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .models import Profile

class ProfileForm(forms.ModelForm):
    """
    The form for a user to fill out their basic profile information
    (name, address, etc.)
    """
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ('full_name', 
                  'email', 
                  'phone_number', 
                  'street_address', 
                  'address2',
                  'country', 
                  'town_or_city',
                  'postcode',)