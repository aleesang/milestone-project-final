from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

from checkout.models import Order

@login_required
def profile(request):
    """A view that displays the profile page of a logged in user"""
    try:
        # retrieves the current user
        user_id = request.user.pk
        # retrieves the Profile object associated with current user
        currentprofile = Profile.objects.get(user=user_id)
        # renders profile.html with the Profile info of the current user
        return render(request, 'profiles/profile.html', {'profile': currentprofile})
    except Profile.DoesNotExist:
        # renders profile.html without Profile information,
        # typically because user has not yet filled in
        # their profile information
        return render(request, 'profiles/profile.html')


def order_history(request):
    """A view that displays the orders page"""
    orders = Order.objects.all().order_by('date')
    order_items = OrderItem.objects.all().order_by('-order')
    return render(request, "order_history",
                  {'orders': orders, 'order_items': order_items})