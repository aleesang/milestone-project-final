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
    default_phone_number = models.CharField(max_length=20, null=True, blank=True, default=None)
    default_street_address = models.CharField(max_length=100, null=True, blank=True, default=None)
    default_address2 = models.CharField(max_length=80, null=True, blank=True, default=None)
    default_country = CountryField(multiple=False, null=True, blank=True, default=None)
    default_town_or_city = models.CharField(max_length=100, null=True, default=None)
    default_postcode = models.CharField(max_length=100, null=True, default=None)


    def __unicode__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        Profile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()