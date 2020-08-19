from django import forms
from django.db import models
class CustomOrderForm(forms.Form):
    subject = forms.CharField(label='*CUSTOM ITEM REQUEST', required=True, widget=forms.TextInput(attrs={'style': 'text-transform:uppercase;'}))
    from_email = forms.EmailField(label='*EMAIL', required=True)
    message = forms.CharField(label='*DESCRIBE YOUR REQUEST', widget=forms.Textarea(attrs={'style': 'text-transform:uppercase;'}), required=True,)
    document = models.FileField(upload_to='documents/')
    