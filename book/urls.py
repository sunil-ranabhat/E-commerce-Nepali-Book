from django.contrib import admin
from django.urls import path
from .views import home, BookList, BookDetail

urlpatterns = [
    path('',home , name='home'),
    path('book/', BookList.as_view() , name = "BookList"),
    path('book/<slug:slug>' , BookDetail.as_view() , name = "BookDetail"),
]