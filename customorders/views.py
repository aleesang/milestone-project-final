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
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "customorders/customorderform.html", {'form': form})

def successView(request):
    return HttpResponse('Success! Thank you for your message.')