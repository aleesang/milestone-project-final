import os
import stripe
import json
import datetime

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from profiles.models import Profile
from profiles.forms import ProfileForm

from .forms import CheckoutForm, MakePaymentForm
from .models import OrderItem, Order, Product
from bag.calculate import inside_bag


@login_required()
def checkout(request):
    """
    The checkout view pulls information from the Order and MakePayment forms
    to process a transaction.
    It is also used to render the checkout.html page,
    displaying bag info and profile details if they exist.
    """
    # requests current user
    user_id = request.user.pk
    # restrieves the Profile info of the current user
    if Profile.objects.filter(user=user_id).exists():
        # condenses Profile info to a single variable
            currentprofile = Profile.objects.get(user=user_id)
            form = ProfileForm(initial={'full_name': currentprofile.full_name,
                                        'email': currentprofile.email,
                                        'phone_number': currentprofile.phone_number,
                                        'street_address': currentprofile.street_address,
                                        'address2': currentprofile.address2,
                                        'country': currentprofile.country,
                                        'town_or_city': currentprofile.town_or_city,
                                        'postcode': currentprofile.postcode,
                                        'user': currentprofile.user})

    else:
        form = CheckoutForm
        
    if request.method == "POST":
        checkout_form = CheckoutForm(request.POST)
        payment_form = MakePaymentForm(request.POST)

        if checkout_form.is_valid() and payment_form.is_valid():
            order = form.save(commit=False)
            order.date = timezone.now()
            order.user = request.user
            order.save()

            bag = request.session.get('bag', {})
            total = 0
            
            for id, quantity in bag.items():
                product = get_object_or_404(Product, pk=id)
                total += quantity * product.price
                order_item = OrderItem(
                    order=order,
                    product=product,
                    quantity=quantity
                )
                order_item.save()

                try:
                    current_bag = bag_contents(request)
                    total = current_bag['final_total']
                    stripe_total = round(total * 100)
                    stripe.api_key = stripe_secret_key
                    intent = stripe.PaymentIntent.create(
                        amount=stripe_total,
                        currency=settings.STRIPE_CURRENCY,
                    )
                except stripe.error.CardError:
                    messages.error(request, 'Your card was declined!')
                if customer.paid:
                    messages.success(request, 'You have successfully paid')
                    request.session['bag'] = {}
                    return redirect(reverse('products'))
                else:
                    messages.error
                    (request,
                     'We are unable to take your payment at this time.')
            else:
                print(payment_form.errors)
                messages.error(
                    request,
                    'We are unable to take payment from this card.')
    else:
        payment_form = MakePaymentForm()
        checkout_form = CheckoutForm()
        
    # auto-fills name and address information
    # if those details have been completed on Checkout page
    return render(request, 
                  "checkout/checkout.html", 
                  {"checkout_form": form, 
                   "payment_form": payment_form, 
                   "publishable": settings.STRIPE_PUBLISHABLE_KEY},
                  )


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
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_email': order.email,
                'default_street_address': order.street_address,
                'default_address2': order.address2,
                'default_country': order.country,
                'default_town_or_city': order.town_or_city,
                'default_postcode': order.postcode,
            }
            user_profile_form = ProfileForm(profile_data, instance=profile)
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