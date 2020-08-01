from __future__ import unicode_literals
from django_countries.fields import CountryField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    """
    This model will contain all of a user's profile information,
    apart from what is required for
    authentication (username, password and email).
    The user does not *need* to fill in these details,
    but they can be used to auto-populate the form found on checkout.html
    We also use a OneToOneField to link it to a specific user!
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=True, blank=True, default=None)
    email = models.EmailField(max_length=254, null=True, blank=True, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=True, default=None)
    street_address = models.CharField(max_length=100, null=True, blank=True, default=None)
    address2 = models.CharField(max_length=80, null=True, blank=True, default=None)
    country = CountryField(multiple=False, null=True, blank=True, default=None)
    town_or_city = models.CharField(max_length=100, null=True, default=None)
    postcode = models.CharField(max_length=100, null=True, default=None)


    def __unicode__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user = Profile.objects.create(user=kwargs['instance'])