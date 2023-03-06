from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import HomeBook
from django.views.generic import ListView , DetailView
from .models import Book
from django.db.models import Q

# Create your views here.

def home(request):
    books= HomeBook.objects.all()
    return render(request,'index.html',{'books':books})

class BookList(ListView):
    model = Book
    template_name = 'books.html'
    #paginate_by = 20
    # def get(self , request , *args , **kwargs):
    #     if not request.GET.get('query'):
    #         return super().get(request , *args , **kwargs)
    #     else:
    #         return super().get(request , *args , **kwargs)
    def get_queryset(self):
        query = self.request.GET.get('query')
        genre= self.request.GET.get('genre')
        if query:
            return Book.objects.filter(Q(english_name__icontains = query) | Q(english_author__icontains = query)).distinct()
        if genre:
            return Book.objects.filter(genre=genre).values()
        return Book.objects.all()

    def get_context_data(self , **kwargs):
        data = super().get_context_data(**kwargs)
        query = self.request.GET.get('query')
        genre= self.request.GET.get('genre')
        if query:
            data['number_of_books']= Book.objects.filter(Q(english_name__icontains = query) | Q(english_author__icontains = query)).count()
        if genre:
            data['number_of_books']= Book.objects.filter(genre=genre).count()
        return data

class BookDetail(DetailView):
    queryset= Book.objects.all()
    template_name = 'book_detail.html'
    data = Book.objects.all()
    count_hit = True

    def get_context_data(self , **kwargs):
        data = super().get_context_data(**kwargs)
        data['similar_books']= Book.objects.all()[:4]
        return data

def sign_in(request):
    return render(request, 'signin.html')
def sign_up(request):
    return render(request, 'signup.html')