from django.contrib import admin
from django.urls import path
from .views import home, BookList, BookDetail,add_to_collection, collection, cart, order

urlpatterns = [
    path('',home , name='home'),
    path('book/', BookList.as_view() , name = "BookList"),
    path('book/<slug:slug>' , BookDetail.as_view() , name = "BookDetail"),
    path('add-to-collection/', add_to_collection , name = "AddToCollection"),
    path('collection/', collection , name = "AddToCollection"),
    path('cart/', cart , name = "AddToCart"),
    path('orders/', order , name = "Orders"),
]