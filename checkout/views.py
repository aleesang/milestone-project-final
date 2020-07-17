from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView, View
from .forms import CheckoutForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    form = CheckoutForm()
    template = 'checkout/checkout.html'
    context = {
        'form': form,
    }

    return render(request, template, context)