from django_countries.fields import CountryField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    """
    This model will contain all of a user's profile information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_full_name = models.CharField(max_length=20, null=True, blank=True, default=None)
    default_email = models.EmailField(max_length=20, null=True, blank=True, default=None)
    default_phone_number = models.CharField(max_length=20, null=True, blank=True, default=None)
    default_street_address = models.CharField(max_length=100, null=True, blank=True, default=None)
    default_address2 = models.CharField(max_length=80, null=True, blank=True, default=None)
    default_country = CountryField(multiple=False, null=True, blank=True, default=None)
    default_town_or_city = models.CharField(max_length=100, null=True, default=None)
    default_postcode = models.CharField(max_length=100, null=True, default=None)


    def __str__(self):
        return self.user.username
    
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Create or update the user profile
    """
    if created:
        Profile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.profile.save()