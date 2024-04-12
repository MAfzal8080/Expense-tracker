from django.contrib import messages
from sqlite3 import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate, login, logout
from .models import *
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='/login')
def home(request):
    profile = Profile.objects.filter(user = request.user).first()
    expenses = Expense.objects.filter(user = request.user) 
    print(request.user)
    if request.method == "POST":
        text = request.POST.get('text')
        amount = request.POST.get("amount")
        expense_type = request.POST.get('expense_type')

        if amount == '' or  text == '' or  expense_type=='':
            context = {'profile': profile, 'expenses': expenses, 'error': 'All fields are required!'}
            return render(request,'home.html',context=context)

        expense = Expense(name=text, amount=amount, expense_type=expense_type, user=request.user)
        expense.save()

        if expense_type == 'Positive':
            profile.balance += float(amount)
        else:
            profile.expenses += float(amount)
            profile.balance -= float(amount)

        profile.save()
        return redirect('/')
    if len(expenses) == 0:
        message = 'No transactions yet! Start adding some.'
        context = {'profile': profile, 'expenses': expenses, 'message': message}
    else:
        context = {'profile': profile, 'expenses': expenses}
    return render(request, 'home.html', context)

def deleteData(request, id):
    data = Expense.objects.get(id=id)
    profile = Profile.objects.filter(user = request.user).first()
    if data.expense_type == 'Positive':
        profile.balance -= float(data.amount)
    else:
        profile.balance += float(data.amount)
        profile.expenses -= float(data.amount)
    profile.save()
    data.delete()
    return redirect('/')

def signup(request):
    return render(request, 'signup.html')

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['cpassword']
        
        # Checking that passwords match
        if password1 != password2:
            return HttpResponse('Passwords do not match' + ', please try again.')

        # Attempt to create new user
        try:
            myuser = User.objects.create_user(username=username, email=email ,password=password1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.save()
            messages.success(request, "Your account has been successfully created! You are now able to log in.")
            login(request, myuser)
            return redirect('/')
        except IntegrityError as e:
            return HttpResponse("Username or Email already exists")  

def handleLogout(request):
    logout(request)
    return redirect('/')  

def handleLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return HttpResponse(f"Invalid credentials {username}")
    else:
        return render(request,'login.html') 

def updateIncome(request):
    if request.method=='POST':
        income = request.POST['amount'];
        profile = Profile.objects.filter(user = request.user).first()
        if profile:
            profile.income = float(income)
            expenses = Expense.objects.filter(user = request.user)
            # totalExpenses = sum([i.amount for i in expenses])
            totalExpenses = 0
            for i in expenses:
                if i.expense_type == 'Negative':
                    totalExpenses -= i.amount
                else:
                    totalExpenses += i.amount
            balance = float(income)-totalExpenses
            profile.balance = balance
        else:
            profile = Profile.objects.create(user=request.user, income=float(income), balance=float(income))
        profile.save()
    return redirect('/')