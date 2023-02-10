from django.shortcuts import render
from django.http import HttpResponse
from .models import HomeBook
from django.views.generic import ListView , DetailView
from .models import Book

# Create your views here.

def home(request):
    books= HomeBook.objects.all()
    return render(request,'index.html',{'books':books})

class BookList(ListView):
    model = Book
    template_name = 'books.html'
    #paginate_by = 20


class BookDetail(DetailView):
    queryset= Book.objects.all()
    template_name = 'book_detail.html'
    data = Book.objects.all()
    count_hit = True

    def get_context_data(self , **kwargs):
        data = super().get_context_data(**kwargs)
        data['padding']= True
        return data