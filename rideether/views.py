from rideether.models import driverDB
from django.shortcuts import redirect, render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from web3 import Web3
import json
import web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.default_account = web3.eth.accounts[1]
abi = json.loads('[{"constant":false,"inputs":[{"name":"_first_name","type":"string"},{"name":"_last_name","type":"string"},{"name":"_email","type":"string"},{"name":"_username","type":"string"},{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"register","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"nbOfUsers","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_driver_name","type":"string"},{"name":"_vehical_name","type":"string"},{"name":"_vehical_number","type":"string"},{"name":"_username","type":"string"},{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"driverRegister","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"login","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"driverInfo","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getLocation","outputs":[{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"driverLogin","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"nbOfDrivers","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getUserAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_fromLocation","type":"string"},{"name":"_toLocation","type":"string"}],"name":"setLocation","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
address = web3.toChecksumAddress("0x11269768d50673270240E7DE9e93a30822E78834")

contract = web3.eth.contract(address=address, abi=abi)

userDetails = []
driverDetails = []
driver = []
checkout = []
locations = []
available = False
tr = ""

def home(request):
    return render(request, 'index.html')

def start(request):
    global available
    global driver
    global tr
    driver = contract.functions.driverInfo().call()
    print(driver)
    tr = driver[5]
    print(tr)
    available = True
    drvDB = driverDB(username=driver[0], driver_name=driver[1] , vehical_name= driver[2], vehical_number=driver[3] , phone_number=driver[4] , driver_address=driver[5] )
    drvDB.save();
    print("DriverDB Saved")
    return redirect('driverIndex')

def stop(request):
    global available
    global driver
    available = False
    
    driverDB.objects.filter(driver_address=driver[5]).delete()
    driver = []

    return redirect('driverIndex')

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
            # if User.objects.filter(username=username).exists():
            #     messages.info(request,'Username Taken')
            #     return redirect('register')
            # elif User.objects.filter(email=email).exists():
            #     messages.info(request,'Email Taken')
            #     return redirect('register')
            # else:
                tx_hash = contract.functions.register(first_name,last_name,email,username,phone_number,password1).transact()
                web3.eth.waitForTransactionReceipt(tx_hash)
                print('User created')
                return redirect('login')
        else:
            messages.info(request,'Password Not Matching')
            return redirect('userRegister')
    else:
        return render(request, "userRegister.html")

def login(request):
    global userDetails
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        userDetails = contract.functions.login(phone_number,password).call()
        print(userDetails)
        if (phone_number == userDetails[3] and password == userDetails[5]):
            return redirect('map')
        else:
            messages.info(request,'Phone Number or Password Not Matching')
            return render(request, 'userLogin.html')
    else:
        return render(request, 'userLogin.html')

def logout(request):
    global userDetails
    userDetails = []
    print(userDetails)
    return redirect('map')

def driverLogout(request):
    global driverDetails
    global available
    available = False
    driverDetails = []
    print(driverDetails)
    return redirect('driverIndex')

def process(request):
    global locations

    checkout = ['Driver','44299','60','BMW','TN37AB1234','117.00','A Location','B Location']
    locations = contract.functions.getLocation().call()
    drv = list(driverDB.objects.values_list())
    print(drv)
    print("~~~~~~~~~~",type(drv))
    if request.method == 'POST':
        return redirect('transact')
    if userDetails:
        return render(request, 'process.html',{'name':userDetails[0],'flag':1,'driver':drv[0],'location':locations})
    else:
        return render(request, 'map.html',{'flag':0,'checkout':checkout})

def map(request):
    if userDetails:
        if request.method == 'POST':
            fromLocation = request.POST['fromLoc']
            toLocation = request.POST['toLoc']
            map_hash = contract.functions.setLocation(fromLocation,toLocation).transact()
            web3.eth.waitForTransactionReceipt(map_hash)
            return redirect("process")
        else:
            return render(request, 'map.html',{'name':userDetails[0],'flag':1})
        
    else:
        return render(request, 'map.html',{'flag':0})

def driverLogin(request):

    global driverDetails
    print(driverDetails)
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']
        driverDetails = contract.functions.driverLogin(phone_number,password).call()
        print(driverDetails)
        if (phone_number == driverDetails[4] and password == driverDetails[5]):
            return redirect('driverIndex')
        else:
            messages.info(request,'Phone Number or Password Not Matching')
            return render(request, 'driverLogin.html')
    else:
        return render(request, 'driverLogin.html')

def driverRegister(request):

    if request.method == 'POST':
        driver_name = request.POST['driver_name']
        vehical_name = request.POST['vehical_name']
        vehical_number = request.POST['vehical_number']
        username = request.POST['username']
        phone_number = request.POST['phone_number']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
                tx_hash = contract.functions.driverRegister(driver_name,vehical_name,vehical_number,username,phone_number,password1).transact()
                web3.eth.waitForTransactionReceipt(tx_hash)
                print('User created')
                return redirect('driverLogin')
        else:
            messages.info(request,'Password Not Matching')
            return redirect('driverRegister')
    else:
        return render(request, "driverRegister.html")

def driverIndex(request):

    if driverDetails:
        return render(request, 'driverIndex.html',{'name':driverDetails[0],'flag':1,'available':available})
    else:
        return render(request, 'driverIndex.html',{'flag':0,'available':available})

def transact(request):
    global tr
    print(web3.eth.default_account, tr)
    if request.method == 'POST':
        transact_hash = web3.eth.send_transaction({'from':web3.eth.default_account, 'to':tr, 'value':1000000000})
        web3.eth.waitForTransactionReceipt(transact_hash)
        print('Transact Success')
    return render(request,'transaction.html')