import os
import stripe
import json
import datetime

from django.contrib import messages
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from profiles.models import Profile
from profiles.forms import ProfileForm

from .forms import CheckoutForm
from .models import OrderItem, Order, Product
from bag.calculate import inside_bag

stripe.api_key = settings.STRIPE_SECRET_KEY
stripe_public_key = settings.STRIPE_PUBLIC_KEY   
stripe_secret_key = stripe.api_key
 
@login_required()
def checkout(request):
    
    """
    The checkout view pulls information from the Order and MakePayment forms
    to process a transaction.
    It is also used to render the checkout.html page,
    displaying bag info and profile details if they exist.
    """

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        total = 0
        print('test', stripe_public_key)
        print('test', stripe.api_key)
        
        form_info = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address': request.POST['street_address'],
            'address2': request.POST['address2'],
            'country': request.POST['country'],
            'town_or_city': request.POST['town_or_city'],
            'postcode': request.POST['postcode'],
        }

        checkout_form = CheckoutForm(form_info)
        if checkout_form.is_valid():
            order = checkout_form.save(commit=False)
            order.date = timezone.now()
            order.user = request.user
            order.save()
            for item_id, item_info in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_info, int):
                        order_item = OrderItem(
                            order=order,
                            product=product,
                            quantity=item_info
                        )
                        order_item.save()
                    else:
                        for size, quantity in item_info['items_by_size'].items():
                            order_item = OrderItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                product_size=size,
                            )
                            order_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))
                    
            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(request, "There's nothing in your bag at the moment")
            return redirect(reverse('products'))
        
        # Create a PaymentIntent with the order amount and currency and the customer id
        current_bag = inside_bag(request)
        total = current_bag['final_total']
        intent = stripe.PaymentIntent.create(
            amount=round(total * 100),
            currency=settings.STRIPE_CURRENCY,
            metadata={'integration_check': 'accept_a_payment'},
            )
        
        
        # Attempt to prefill the form with any info the user maintains in their profile
        if request.user.is_authenticated:
            try:
                currentprofile = Profile.objects.get(user=request.user)
                checkout_form = CheckoutForm(initial={
                        'full_name': currentprofile.full_name,
                        'email': currentprofile.email,
                        'phone_number': currentprofile.phone_number,
                        'street_address': currentprofile.street_address,
                        'address2': currentprofile.address2,
                        'country': currentprofile.country,
                        'town_or_city': currentprofile.town_or_city,
                        'postcode': currentprofile.postcode,
                        'user': currentprofile.user
                        })
            except Profile.DoesNotExist:
                checkout_form = CheckoutForm()
        else:
            checkout_form = CheckoutForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'checkout_form': checkout_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)

def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_info = {
                'default_phone_number': order.phone_number,
                'default_email': order.email,
                'default_street_address': order.street_address,
                'default_address2': order.address2,
                'default_country': order.country,
                'default_town_or_city': order.town_or_city,
                'default_postcode': order.postcode,
            }
            user_profile_form = ProfileForm(profile_info, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
