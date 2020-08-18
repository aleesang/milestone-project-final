from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import CustomOrderForm

def customOrderView(request):
    if request.method == 'GET':
        form = CustomOrderForm()
    else:
        form = CustomOrderForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            custom_item_request = form.cleaned_data['custom_item_request']
            quantity = form.cleaned_data['quantity']
            describe_request = form.cleaned_data['describe_request']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "customorders/customorderform.html", {'form': form})

def successView(request):
    return render(request, "checkout/checkout_success.html", {'form': form})