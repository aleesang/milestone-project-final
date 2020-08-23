from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from profiles.models import Profile
from profiles.forms import ProfileForm

from .forms import CheckoutForm
from .models import OrderItem, Order, Product
from bag.calculate import inside_bag
   
import stripe
import json
import datetime


"""
The code in this document was inspired by code institute tutorial on stripe, 
which helped me get the payment method to work. It also enabled me to get the view to work
on checkout_success.
"""


@require_POST
def cache_checkout_data(request):
    """
    View to process payment method.
    """    
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)
    
@login_required()
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY   
    stripe_secret_key = settings.STRIPE_SECRET_KEY 
    """
    The checkout view pulls information from the Order forms
    to process a transaction.
    It is also used to render the checkout.html page,
    displaying bag info and profile details if they exist.
    """

    if request.method == 'POST':
        bag = request.session.get('bag', {})
        total = 0
        
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
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)
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
                    
            # Save the info to the user's profile 
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
        
        # Create a PaymentIntent with the order amount and currency
        current_bag = inside_bag(request)
        total = current_bag['final_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
                    amount=stripe_total,
                    currency='aud',
        )
         
        # Try and refill the form with the user information in their profile
        if request.user.is_authenticated:
            try:
                currentprofile = Profile.objects.get(user=request.user)
                checkout_form = CheckoutForm(initial={
                        'full_name': currentprofile.user.get_full_name,
                        'email': currentprofile.user.email,
                        'phone_number': currentprofile.default_phone_number,
                        'street_address': currentprofile.default_street_address,
                        'address2': currentprofile.default_address2,
                        'country': currentprofile.default_country,
                        'town_or_city': currentprofile.default_town_or_city,
                        'postcode': currentprofile.default_postcode,
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
    A view to confirm a successful checkout
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        currentprofile = Profile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = currentprofile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'default_full_name': order.full_name,
                'default_email': order.email,
                'default_phone_number': order.phone_number,
                'default_street_address': order.street_address,
                'default_address2': order.address2,
                'default_country': order.country,
                'default_town_or_city': order.town_or_city,
                'default_postcode': order.postcode,
            }
            user_profile_form = ProfileForm(profile_data, instance=currentprofile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Success! Your orser is now processed! \
        Your order number is {order_number}.')

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
