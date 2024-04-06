from django.shortcuts import render, redirect
from .models import *

# Create your views here.

def home(request):
    profile = Profile.objects.filter(user = request.user).first()
    expenses = Expense.objects.filter(user = request.user) 
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