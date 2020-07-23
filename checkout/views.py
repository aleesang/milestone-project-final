from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from django.views.generic import ListView, DetailView, View
from .forms import CheckoutForm
from .models import Order, OrderItem
from products.models import Product
from django.utils import timezone
from bag.calculate import inside_bag
import stripe


def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address': request.POST['street_address'],
            'address2': request.POST['address2'],
            'town_or_city': request.POST['town_or_city'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
        }      
        form = CheckoutForm(form_data)
        if form.is_valid():
            order = form.save()
            for item_id, item_data in bag.items():
                product = Product.objects.get(id=item_id) 
                order_item = OrderItem(
                    order = order,
                    feature = feature,
                    quantity = quantity
                )
                order_item.save()
                
            try:

            # Attempt to charge the user
                
                current_bag = inside_bag(request)
                total = current_bag['final_total']
                stripe_total = round(total * 100)
                stripe.api_key = stripe_secret_key
                intent = stripe.PaymentIntent.create(
                    amount=stripe_total,
                    currency=settings.STRIPE_CURRENCY,
                    )  

            except stripe.error.CardError:
                messages.error(request, "Your credit card was declined")
                
                request.session['save_info'] = 'save-info' in request.POST
                return redirect(reverse('checkout_success', args=[order.order_number]))

            # If payment succeeds, add the purchased votes to the feature's total votes
            else:
                if intent.paid:
                    messages.success(request, "You have successfully paid. Thank you for purchasing upvotes!")
    
                else:
                    messages.error(request, "Error with transaction")

        else:
            messages.error(request, "Error in taking payment from specified card")



    return render(request, template, context)
    template = 'checkout/checkout.html'
    context = {
                'form': form,
                'stripe_public_key': stripe_public_key,
                'stripe_secret_key': stripe_secret_key,
            }


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