from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import CustomOrderForm
from django.core.files.storage import FileSystemStorage


def customOrderView(request):
    if request.method == 'GET':
        form = CustomOrderForm()
        to = request.get('recipient_email')
    else:
        form = CustomOrderForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email, ['admin@gmail.com',])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "customorderform.html", {'form': form})

def successView(request):
    return render(request, "success.html")

