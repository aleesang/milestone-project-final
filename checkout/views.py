from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect, render
from django.contrib import messages
from django.conf import settings
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
from .models import OrderItem, Order, Product
from django.utils import timezone
from bag.calculate import inside_bag
import stripe

# api for stripe, gets secret_key from settings
stripe.api_key = 'sk_test_51Gzgb6Dylq7SXtdaSvFbSZSTV6Pg65KpqoPkHQVmY5ShuTSEqXPSf4BDjccfFnMQpeSrLSU35ynzzniihvOUGn4Q00BZM5zgfo'

def checkout(request):
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address': request.POST['street_address'],
            'address2': request.POST['address2'],
            'country': request.POST['country'],
            'town_or_city': request.POST['town_or_city'],
            'postcode': request.POST['postcode'],
        }

        form = CheckoutForm(form_data)
        if form.is_valid():
            order = form.save()
            for item_id, item_data in bag.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_item = OrderItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_item.save()
                    
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your bag wasn't found in our database. "
                        "Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

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

        current_bag = inside_bag(request)
        total = current_bag['final_total']
        stripe_total = round(total * 100)
        charge = stripe.Charge.create(
        amount=2000,
        currency="aud",
        description="My First Test Charge (created for API docs)",
        source="tok_visa", # obtained with Stripe.js
        idempotency_key='xuDNY8KRXLPrYH6u'
        )
        
        form = CheckoutForm()

    if not stripe_publishable_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'form': form,
        'stripe_publishable_key': stripe_publishable_key,
    }

    return render(request, template, context)


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