from django.shortcuts import render

# Create your views here.

def map(request):
    return render(request, 'map.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def process(request):
    return render(request, 'process.html')