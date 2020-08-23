from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

from checkout.models import Order

@login_required
def profile(request):
    """A view that displays the profile page of a logged in user"""
    profile = get_object_or_404(Profile, user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was uodated successfully!')
        else:
            messages.error(request, 'Incomplete. Please check your details are correct and all fields are filled in.')
    else:
        form = ProfileForm(instance=profile)
    orders = profile.orders.all()

    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)

def order_history(request, order_number):
    """A view that displays the order history"""
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is previous confirmation for order number {order_number}. '
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)