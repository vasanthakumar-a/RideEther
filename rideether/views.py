from django.shortcuts import redirect, render, redirect
from django.contrib.auth.models import User, auth
# Create your views here.

def map(request):
    return render(request, 'map.html')

def register(request):

    if request.method == 'POST':
        first_name=request.POST.get["first_name"]
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1==password2:
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name, phone_number=phone_number)
            user.save()
        print("user created")
        return redirect('/')

    else:
        return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def process(request):
    return render(request, 'process.html')