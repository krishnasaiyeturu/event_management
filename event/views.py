from django.db.models import query
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,logout

from django.http import HttpResponseRedirect

# Create your views here.


@csrf_exempt
def login(request):
    logout(request)
    return render(request,'login.html')

@csrf_exempt
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login')


@login_required(login_url='/login')
def index(request):
    return render(request,'index.html')

@login_required(login_url='/login')
def event(request):
    return render(request,'event.html')

@login_required(login_url='/login')
def venues(request):
    return render(request,'venues.html')

@login_required(login_url='/login')
def prices(request):
    return render(request,'prices.html')

@login_required(login_url='/login')
def book_event(request):
    return render(request,'book_event.html')
