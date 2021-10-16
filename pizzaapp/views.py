from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import PizzaModel, CustomerModel, OrderModel


# Create your views here.


def adminloginview(request):
    return render(request, "pizzaapp/adminlogin.html")


def authenticateadmin(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    # user exist
    if user is not None and user.username == "tadakasuryateja":
        login(request, user)
        return redirect('adminhomepage')
    # user doesnot exist
    elif user is None:
        messages.add_message(request, messages.ERROR, "Invalid Credentials")
        return redirect('adminloginpage')
    else:
        return redirect('adminloginpage')


def adminhomepageview(request):
    context = {'pizzas': PizzaModel.objects.all()}
    return render(request, "pizzaapp/adminhomepage.html", context)


def logoutadmin(request):
    logout(request)
    return redirect('adminloginpage')


def addpizza(request):
    # write code to add the pizza into the database
    name = request.POST['pizza']
    price = request.POST['price']
    PizzaModel(name=name, price=price).save()
    return redirect('adminhomepage')


def deletepizza(request, pizzapk):
    PizzaModel.objects.filter(id=pizzapk).delete()
    return redirect('adminhomepage')


def homepageview(request):
    return render(request, "pizzaapp/homepage.html")


def signupuser(request):
    username = request.POST['username']
    password = request.POST['password']
    phoneno = request.POST['phoneno']
    # if username exists
    if User.objects.filter(username=username).exists():
        messages.add_message(request, messages.ERROR, "User Already Exists")
        return redirect('homepage')

    # if username doesnot exists already
    User.objects.create_user(username=username, password=password).save()
    lastobject = len(User.objects.all()) - 1
    CustomerModel(userid=User.objects.all()[int(lastobject)].id, phoneno=phoneno).save()
    messages.add_message(request, messages.ERROR, "User successfully created")
    return redirect('homepage')


def userloginview(request):
    return render(request, 'pizzaapp/userlogin.html')


def userauthenticate(request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    # user exist
    if user is not None:
        login(request, user)
        return redirect('customerpage')
    # user doesnot exist
    else:
        messages.add_message(request, messages.ERROR, "Invalid Credentials")
        return redirect('userloginpage')


def customerwelcomeview(request):
    if not request.user.is_authenticated:
        return redirect('userloginpage')
    username = request.user.username
    context = {'username': username, 'pizzas': PizzaModel.objects.all()}
    return render(request, 'pizzaapp/customerwelcome.html', context)


def userlogout(request):
    logout(request)
    return redirect('userloginpage')


def placeorder(request):
    if not request.user.is_authenticated:
        return redirect('userloginpage')

    username = request.user.username
    phoneno = CustomerModel.objects.filter(userid=request.user.id)[0].phoneno
    address = request.POST['address']
    ordereditems = ''
    for pizza in PizzaModel.objects.all():
        pizzaid = pizza.id
        name = pizza.name
        price = pizza.price
        quantity = request.POST.get(str(pizzaid), " ")
        print(name, price, quantity)
        if str(quantity) != "0" and str(quantity) != " ":
            ordereditems = ordereditems + name + " " + " price : " + str(
                int(price) * int(quantity)) + " quantity : " + quantity + "   "

    OrderModel(username=username, phoneno=phoneno, address=address, ordereditems=ordereditems).save()
    messages.add_message(request, messages.SUCCESS, "Order Successfully Placed")
    return redirect('customerpage')


def userorders(request):
    orders = OrderModel.objects.filter(username=request.user.username)
    context = {'orders': orders}
    return render(request, 'pizzaapp/userorders.html', context)


def adminorder(request):
    orders = OrderModel.objects.all()
    context = {"orders": orders}
    return render(request, 'pizzaapp/adminorders.html', context)


def acceptorder(request, orderpk):
    order = OrderModel.objects.filter(id=orderpk)[0]
    order.status = "accepted"
    order.save()
    return redirect(request.META['HTTP_REFERER'])


def declineorder(request, orderpk):
    order = OrderModel.objects.filter(id=orderpk)[0]
    order.status = "declined"
    order.save()
    return redirect(request.META['HTTP_REFERER'])
