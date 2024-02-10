from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from .models import HomeBook
from django.views.generic import ListView , DetailView
from .models import Book, Review, Order
from django.db.models import Q
from user.models import User
from .recommendation import  content_recommendation, collaborative_recommendation

# Create your views here.

def home(request):
    books= Book.objects.all().order_by('-avg_rating')[:4]
    print(books)
    if request.user.is_authenticated:
            print(User.objects.get(id=request.user.id).collection.all().count())
            no_of_collection= User.objects.get(id=request.user.id).collection.all().count()
            if no_of_collection>0:
                no_of_collection+=1
                ratings= collaborative_recommendation(request.user.id)
                suggestions=[]
                for i in range(4):
                    suggestions.append(Book.objects.get(id=ratings[i*no_of_collection][1]))
                return render(request,'index.html',{'books':books,'suggestions': suggestions})
    return render(request,'index.html',{'books':books})

def collection(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        context= user.collection.all()
    else:
        return redirect('/auth/signin/?next=/collection/')
    return render(request,'collection.html',{'books':context})

def order(request):
    if request.method== 'POST':
        order_id= request.POST.get('order_id')
        Order.objects.filter(id=order_id).delete()
        return redirect('/orders')
    orders= Order.objects.all()
    print(orders)
    return render(request,'order.html',{'orders':orders})



def cart(request):
    if request.user.is_authenticated:
        user=User.objects.get(id=request.user.id)
        context= user.cart.all()
    else:
        return redirect('/auth/signin/?next=/cart/')
    if request.method=='POST':
        user = User.objects.get(id=request.user.id)
        new_order = Order(user=user)
        new_order.save()
        
        books_ids = request.POST.getlist('books')
        books = Book.objects.filter(id__in=books_ids)
        new_order.books.set(books)
        user.cart.clear()
        return HttpResponse('You have successfully order books')

    return render(request,'cart.html',{'books':context})


class BookList(ListView):
    model = Book
    template_name = 'books.html'
    

    def get_queryset(self):
        query = self.request.GET.get('query')
        genre= self.request.GET.get('genre')
        print(genre)
        if query:
            return Book.objects.filter(Q(english_name__icontains = query) | Q(english_author__icontains = query)).distinct()
        if genre:
            print(Book.objects.filter(Q(genre__icontains = genre)))
            return Book.objects.filter(Q(genre__icontains = genre)).values()
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
        id= Book.objects.get(slug=self.kwargs.get('slug')).id
        if not self.request.user.is_authenticated:
            data['has_in_collection']=False
            data['has_in_cart']= False
        else:
            user=User.objects.get(id=self.request.user.id)
            book= Book.objects.get(slug=self.kwargs.get('slug'))
            if book in user.collection.all():
                data['has_in_collection']=True
            else:
                data['has_in_collection']=False
            if book in user.cart.all():
                data['has_in_cart']=True
            else:
                data['has_in_cart']=False
            
        data['id'] =id
        data['reviews'] = Review.objects.filter(book=self.get_object())
        

        user_id=1
        if self.request.user.is_authenticated:
            user_id= self.request.user.id
        


        book = self.get_object()
        values= content_recommendation(book.english_name)
        suggestions=[]
        for i in range(4):
            suggestions.append(Book.objects.get(id=values[i+1][1]))
        print(suggestions)
        data['suggestions']= suggestions
        # if self.request.user.is_authenticated:
        #     print(User.objects.get(id=user_id).collection.all().count())
        #     no_of_collection= User.objects.get(id=user_id).collection.all().count()+1
        #     ratings= get_ratings(user_id)
        #     suggestions=[]
        #     for i in range(4):
        #         suggestions.append(Book.objects.get(id=ratings[i*no_of_collection][1]))
        #     print(suggestions)
        #     data['suggestions']= suggestions
        #print(ratings)
        return data
    def post(self , request , *args , **kwargs):
        if self.request.POST.__contains__('rating'):
            #print(self.request.POST['rating']=='')
            rating_text= self.request.POST['review_text']
            rating_value= self.request.POST['rating']
            if(rating_value==''):
                rating_value=0
            new_review = Review(book= self.get_object(), author = self.request.user, review_text= rating_text , review=rating_value)
            new_review.save()
        # elif self.request.POST.__contains__('cart'):
        #     book_id= self.request.POST.get('book_id')
        #     user=User.objects.get(id=self.request.user.id)
        #     user.cart.add(book_id)
        else:
            book_id= self.request.POST.get('book_id')
            user=User.objects.get(id=self.request.user.id)
            user.cart.add(book_id)
        return redirect(request.path_info)

def add_to_collection(request):
    print(request.user)


