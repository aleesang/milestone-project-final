from django import forms

class CustomOrderForm(forms.Form):
    full_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    custom_item_request = forms.CharField(required=True)
    quantity = forms.CharField(required=True)
    describe_request = forms.CharField(widget=forms.Textarea, required=True)