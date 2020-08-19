from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import CustomOrderForm
from django.core.files.storage import FileSystemStorage


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
                send_mail(from_email, subject, message, ['admin@example.com'])
            
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('success')
    return render(request, "customorders/customorderform.html", {'form': form})

def successView(request):
    return render(request, "checkout/checkout_success.html", {'form': form})


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'customorders/customorderform.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, "customorders/customorderform.html", {'form': form})
