from django.contrib import admin
from django.urls import path
from .views import home, BookList, BookDetail,sign_in,sign_up

urlpatterns = [
    path('',home , name='home'),
    path('book/', BookList.as_view() , name = "BookList"),
    path('book/<slug:slug>' , BookDetail.as_view() , name = "BookDetail"),
    # path('signin/', sign_in , name = "Signin"),
    # path('signup/', sign_up , name = "Signup"),
]