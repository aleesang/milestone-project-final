from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect, render
from django.contrib import messages
from django.conf import settings
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm, MakePaymentForm
from .models import OrderItem, Order, Product
from django.utils import timezone
from bag.calculate import inside_bag
import stripe


# api for stripe, gets secret_key from settings
stripe.api_key = 'sk_test_51Gzgb6Dylq7SXtdaSvFbSZSTV6Pg65KpqoPkHQVmY5ShuTSEqXPSf4BDjccfFnMQpeSrLSU35ynzzniihvOUGn4Q00BZM5zgfo'

def checkout(request):
    """
    The checkout view pulls information from the Order and MakePayment forms
    to process a transaction.
    It is also used to render the checkout.html page,
    displaying bag info and checkout details if they exist.
    """
    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {'full_name': request.POST['full_name'],
                                    'email': request.POST['email'],
                                    'phone_number': request.POST['phone_number'],
                                    'street_address': request.POST['street_address'],
                                    'address2': request.POST['address2'],
                                    'country': request.POST['country'],
                                    'town_or_city': request.POST['town_or_city'],
                                    'postcode': request.POST['postcode'],}

        form = CheckoutForm
    if request.method == "POST":
        payment_form = MakePaymentForm(request.POST)

        if payment_form.is_valid():
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
                customer = stripe.Charge.create(
                    amount=stripe_total,
                    currency=settings.STRIPE_CURRENCY,
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id']
                )
            # Provides various messages to user dependent on success of order
            except stripe.error.CardError:
                messages.error(request, "Your card was declined!")

            if customer.paid:
                messages.error(request, "Your Order was Successful")
                request.session['bag'] = {}
                return redirect(reverse('checkout'))
            else:
                messages.error(request, "Unable to take payment")
        else:
            print(payment_form.errors)
            messages.error(request,
                           "We were unable to take a payment with that card!")
    else:
        payment_form = MakePaymentForm()
        form = CheckoutForm()

    # auto-fills name and address information
    # if those details have been completed on Checkout page
    return render(request, "checkout.html", 
                  {"payment_form": payment_form, "publishable": settings.STRIPE_PUBLISHABLE_KEY})
    
def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
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
    