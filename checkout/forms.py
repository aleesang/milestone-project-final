from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .models import Order

PAYMENT = (
    ('S', 'Stripe')
)
class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                            'street_address', 'address2',
                            'town_or_city', 'country', 'postcode',)  
                
        full_name = forms.CharField(widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name'
            }))

        email = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }))

        phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone Number'
            }))

        street_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Address'
            }))

        address2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Alternative Address'
            }))

        town_or_city = forms.CharField(required=False, widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Town/City'
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

