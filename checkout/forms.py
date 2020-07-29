from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Order

from django import forms
from .models import Order

class MakePaymentForm(forms.Form):
    """
    The form for making payments,
    requires user to input their (valid) credit card information
    """
    MONTH_CHOICES = [(i, i) for i in range(1, 12)]
    YEAR_CHOICES = [(i, i) for i in range(2020, 2036)]

    credit_card_number = forms.CharField(label='Credit card number',
                                         required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month', choices=MONTH_CHOICES,
                                     required=False)
    expiry_year = forms.ChoiceField(label='Year', choices=YEAR_CHOICES,
                                    required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)
    
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 
                  'email', 
                  'phone_number', 
                  'street_address', 
                  'address2',
                  'country', 
                  'town_or_city',
                  'postcode',) 

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'street_address': 'Street Address',
            'address2': 'Alternate Street Address',
            'country': 'Country',
            'town_or_city': 'Town or City',
            'postcode': 'Postal Code',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False

