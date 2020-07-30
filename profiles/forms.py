from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import check_password
from .models import Profile


class UserLoginForm(forms.Form):
    """
    Form for a registered user to login
    """
    username_or_email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
    """
    Form for a user to register for an account
    Ensures that email is of a valid syntax
    Ensures that passwords match
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password Confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password1 or not password2:
            raise ValidationError("Password must not be empty")

        if password1 != password2:
            raise ValidationError("Passwords do not match")

        return password2


class UserUpdateForm(forms.Form):
    """
    Form for a user to edit their email and password
    """
    email = forms.EmailField()
    current_password = forms.CharField(widget=forms.PasswordInput,
                                       required=False)
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput, required=False)
    new_password2 = forms.CharField(label="Confirm new password",
                                    widget=forms.PasswordInput, required=False)

    # make sure we can pass the User instance in to the form
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(UserUpdateForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        old = self.cleaned_data.get("current_password")
        if not old or check_password(old, self.user.password):
            return old
        else:
            raise forms.ValidationError("Please enter "
                                        "your correct current password")

    def clean_new_password2(self):
        first = self.cleaned_data.get("new_password1")
        second = self.cleaned_data.get("new_password2")
        if first != second:
            raise forms.ValidationError("The passwords must match!")
        return second


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