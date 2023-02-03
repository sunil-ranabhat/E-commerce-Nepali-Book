from django.shortcuts import render
from django.http import HttpResponse
from .models import HomeBook

# Create your views here.

def home(request):
    books= HomeBook.objects.all()
    return render(request,'index.html',{'books':books})