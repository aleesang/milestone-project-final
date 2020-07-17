from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Order

PAYMENT = (
    ('S', 'Stripe')
)
model = Order
fields = ('full_name', 'email', 'phone_number',
                  'street_address', 'address2',
                  'town_or_city', 'country', 'postcode',)
        
class CheckoutForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your First and Last Name'
    }))

    email = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your email adddress'
    }))

    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contact Number'
    }))
    
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Address'
    }))

    address_2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Alternate Address (Optional)'
    }))

    town_or_city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Town or City'
    }))

    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    
    postcode = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT)