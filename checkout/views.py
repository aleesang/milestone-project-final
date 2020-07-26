from django.shortcuts import render, redirect, reverse, get_object_or_404, redirect, render
from django.contrib import messages
from django.conf import settings
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
from .models import Product, OrderItem, Order
from django.utils import timezone
from bag.calculate import inside_bag
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


@login_required()
def checkout(request):
    bag_page = "active"
    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = form.save(commit=False)
            order.date = timezone.now()
            order.save()

            bag = request.session.get('bag', {})
            total = 0
            # Calculate the total charge
            for id, quantity in bag.items():
                product = get_object_or_404(Products, pk=id)
                order_item, created = OrderItem.objects.get_or_create(
                    order = order,
                    product = product,
                    quantity = quantity
                )
                order_item.save()
            # Attempt to charge the user
            try:
                customer = stripe.Charge.create(
                    amount = int(total * 100),
                    currency = "aud",
                    description = request.user.email,
                    card = form.cleaned_data['stripe_id'],                    
                )
            except stripe.error.CardError:
                messages.error(request, "Your credit card was declined")
            
            # If payment succeeds, add the purchased votes to the product's total votes
            else:
                if customer.paid:
                    messages.success(request, "You have successfully paid. Thank you for purchasing upvotes!")
    
                    #Add the Votes
                    for id, quantity in bag.items():
                        product = get_object_or_404(pk=id)
                        product.save()
    
                    #Continue to clear bag and move on                 
                    request.session['bag'] = {}
                    return redirect('checkout_success')
                else:
                    messages.error(request, "Error with transaction")

        else:
            messages.error(request, "Error in taking payment form specified card")

    else:
        form = CheckoutForm()
        context = {
            'form': form
        }
        return render(request, 'checkout/checkout.html', context)

# Once payment is complete, direct user to a page to acknowledge it
def  checkout_success(request):
    return render(request, "checkout/checkout_success.html")
