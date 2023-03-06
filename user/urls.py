from django.contrib import admin
from django.urls import path
from .views import signup,signin,logout

urlpatterns = [
    path('signin/', signin , name = "Signin"),
    path('signup/', signup , name = "Signup"),
    path('logout/', logout , name = "Logout"),
]