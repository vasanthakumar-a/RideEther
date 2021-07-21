from typing import Container
from django.shortcuts import redirect, render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from web3 import Web3
import json
import web3
# Create your views here.

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.default_account = web3.eth.accounts[0]
abi = json.loads('[{"constant":false,"inputs":[{"name":"_first_name","type":"string"},{"name":"_last_name","type":"string"},{"name":"_email","type":"string"},{"name":"_username","type":"string"},{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"register","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"nbOfUsers","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"login","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getUserAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
address = web3.toChecksumAddress("0xF4edE9Db5D05419F06dC11D9d18a263f6D739E80")

contract = web3.eth.contract(address=address, abi=abi)

details = []
checkout = []

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        username = request.POST['username']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:
                tx_hash = contract.functions.register(first_name,last_name,email,username,phone_number,password1).transact()
                web3.eth.waitForTransactionReceipt(tx_hash)
                # user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                # user.save()
                print('User created')
                return redirect('login')
        else:
            messages.info(request,'Password Not Matching')
            return redirect('userRegister')
    else:
        return render(request, "userRegister.html")

def login(request):
    global details
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        details = contract.functions.login(phone_number,password).call()
        print(details)
        if (phone_number == details[3] and password == details[5]):
            return redirect('process')
        else:
            messages.info(request,'Phone Number or Password Not Matching')
            return render(request, 'userLogin.html')
    else:
        return render(request, 'userLogin.html')

def logout(request):
    global details
    details = []
    print(details)
    return redirect('map')

def process(request):
    
    checkout = ['Driver','44299','60','BMW','TN37AB1234','117.00','A Location','B Location']

    print(details)
    if details:
        return render(request, 'process.html',{'name':details[0],'flag':1,'checkout':checkout})
    else:
        return render(request, 'process.html',{'flag':0,'checkout':checkout})

def map(request):
    print(details)
    if details:
        return render(request, 'map.html',{'name':details[0],'flag':1})
    else:
        return render(request, 'map.html',{'flag':0})

def driverLogin(request):
    return render(request, 'driverLogin.html')

def driverRegister(request):
    return render(request, 'driverRegister.html')

def driverIndex(request):
    if details:
        return render(request, 'driverIndex.html',{'name':details[0],'flag':1,'checkout':checkout})
    else:
        return render(request, 'driverIndex.html',{'flag':0,'checkout':checkout})