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
abi = json.loads('[{"constant":false,"inputs":[{"name":"_first_name","type":"string"},{"name":"_last_name","type":"string"},{"name":"_email","type":"string"},{"name":"_username","type":"string"},{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"register","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"nbOfUsers","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"login","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getUsername","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getUserAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
address = web3.toChecksumAddress("0x43c0843DB400F7FF865DdA78DD4e528162d4e70e")

contract = web3.eth.contract(address=address, abi=abi)

details = []

def map(request):
    return render(request, 'map.html')

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
            return redirect('register')
    else:
        return render(request, "register.html")

def login(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        tx_hash = contract.functions.login(phone_number,password).transact()
        web3.eth.waitForTransactionReceipt(tx_hash)
        print(web3.utils.hexToNumberString(tx_hash))

        return redirect('register')
    else:
        return render(request, 'login.html')

def process(request):
    return render(request, 'process.html')