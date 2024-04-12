from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('deleteData/<int:id>', deleteData, name='deleteData'),
    path('signup', signup, name='signup'),
    path('login', handleLogin, name="handleLogin"),
    path('logout', handleLogout, name='handleLogout'), 
    path('register', register, name="register"),
    path('updateIncome', updateIncome, name="updateIncome"),
]