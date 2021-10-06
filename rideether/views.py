from web3.module import retrieve_async_method_call_fn
from rideether.models import acceptDB, driverDB, waitingDB
from django.shortcuts import redirect, render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from web3 import Web3
import json
import web3

ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
web3.eth.default_account = web3.eth.accounts[0]
abi = json.loads('[{"constant":false,"inputs":[{"name":"_first_name","type":"string"},{"name":"_last_name","type":"string"},{"name":"_email","type":"string"},{"name":"_username","type":"string"},{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"register","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"nbOfUsers","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"rate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_driver_name","type":"string"},{"name":"_vehical_name","type":"string"},{"name":"_vehical_number","type":"string"},{"name":"_username","type":"string"},{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"driverRegister","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_rate","type":"uint256"}],"name":"setRate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"login","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getRate","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"driverInfo","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getLocation","outputs":[{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_phone_number","type":"string"},{"name":"_password","type":"string"}],"name":"driverLogin","outputs":[{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"nbOfDrivers","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getUserAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_fromLoc","type":"string"},{"name":"_toLoc","type":"string"}],"name":"setLocation","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
address = web3.toChecksumAddress("0x64B4556Aa9E57f7dB19b90022bc59742EAe09c51")

contract = web3.eth.contract(address=address, abi=abi)

userDetails = []
driverDetails = []
driver = []
checkout = []
locations = []
available = False
trans = False
tr = ""

def home(request):
    return render(request, 'index.html')

def start(request):
    global available
    global driver
    driver = contract.functions.driverInfo().call()
    print(driver)

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
    global trans
    global tr

    checkout = ['Driver','44299','60','BMW','TN37AB1234','117.00','A Location','B Location']
    locations = contract.functions.getLocation().call()
    ratings = contract.functions.getRate().call()
    drv = list(driverDB.objects.values_list())
    if userDetails:
        if request.method == 'POST':
            if drv:
                wait = waitingDB(first_name=userDetails[1], last_name=userDetails[2], email=userDetails[4], username=userDetails[0], phone_number=userDetails[3],drv_username=drv[0][4])
                wait.save()
                return redirect('accept')
            else:
                return redirect('process')
        else:
            if drv:
                tr = drv[0][6]
                return render(request, 'process.html',{'name':userDetails[0],'flag':1,'driver':drv[0],'location':locations,'rate':ratings})
            else:
                return render(request, 'process.html',{'name':userDetails[0],'flag':1,'location':locations})
    else:
        return render(request, 'map.html',{'flag':0,'checkout':checkout})

def accept(request):
    global trans

    accp = list(acceptDB.objects.values_list())
    if accp:
        trans = True
        acceptDB.objects.filter(user_address=web3.eth.default_account).delete()
        return redirect('transact')
    else:
        return render(request, 'accept.html')

def waiting(request):
    return render(request, 'waiting.html')

def acceptRide(request):
    global notice

    wait = list(waitingDB.objects.values_list())
    if request.method == 'POST':
        stop(request)
        f_addr = contract.functions.getUserAddress().call()
        accp = acceptDB(driver_address=web3.eth.default_account ,user_address=f_addr ,accept=1)
        accp.save()
        waitingDB.objects.filter(drv_username=wait[0][6]).delete()
        notice = 0
        return redirect('driverIndex')
    else:
        return render(request, 'acceptRide.html',{'main_info':wait[0]})

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
    global notice

    wait = list(waitingDB.objects.values_list())
    print(wait)
    if driverDetails:
        if wait:
            notice = 1
            return render(request, 'driverIndex.html',{'name':driverDetails[0],'flag':1,'notice':notice,'available':available,'wait':wait})
        else:
            return render(request, 'driverIndex.html',{'name':driverDetails[0],'flag':1,'available':available})
    else:
        return render(request, 'driverIndex.html',{'flag':0,'available':available})

def transact(request):
    global tr
    global trans

    print(web3.eth.default_account, tr)
    if request.method == 'POST':
        transact_hash = web3.eth.send_transaction({'from':web3.eth.default_account, 'to':tr, 'value':1000000000000000000})
        web3.eth.waitForTransactionReceipt(transact_hash)
        print('Transact Success')
        return redirect('rate')
    else:
        amount = 1
        t_from = web3.eth.default_account
        if trans:
            return render(request,'transaction.html',{'amount':amount,'from':t_from[-5:],'to':tr[-5:]})
        else:
            return redirect('login')

def rate(request):
    global rating
    if request.method == 'POST':
        rating = request.POST['rating']
        print(rating)
        setRate(int(rating))
        return redirect('/')
    else:
        return render(request,'rate.html')

def setRate(rating):
    rates = contract.functions.getRate().call()
    rates = (rates+rating)//2
    print(rates)

    rate_hash = contract.functions.setRate(rates).transact()
    web3.eth.waitForTransactionReceipt(rate_hash)