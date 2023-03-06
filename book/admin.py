from django.contrib import admin
from .models import Book
from django.urls import path,reverse
from django.shortcuts import redirect,render
from .models import Book,HomeBook
from  django.http import HttpResponseRedirect
from django import forms
from random import randrange
# Register your models here.
class BookForm(forms.Form):
    book_upload = forms.FileField()


genres=['Fiction', 'Non-Fiction', 'Novel', 'Fantasy','Biography','Poetry']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('english_name','nepali_name',)
    search_fields=('english_name',)
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('upload-book/',self.upload_book),
           
        ]
        return new_urls + urls
    
    def upload_book(self,request):
        if request.method=='POST':
            books = request.FILES["book_upload"]
            if not books.name.endswith('.csv'):
                return redirect('/admin')
            
            file_data = books.read().decode('utf-8')
            csv_data = file_data.split("\n")

            for x in csv_data:
                
                fields = x.split(";")
                if fields[12]=='':
                    fields[12]=100
                # print(fields[0])
                Book.objects.create(
                    ISBN= fields[0],
                    english_name= fields[2],
                    nepali_name= fields[1],
                    english_author= fields[3],
                    nepali_author=fields[5],
                    genre= genres[randrange(0,6)],
                    avg_rating=float(fields[9].replace(',','.')),
                    slug=fields[2].replace(' ','-'),
                    Publisher= fields[10],
                    no_of_pages=fields[12],
                    year_published=fields[14],
                    image='',

                )
            url = reverse('admin:index')
            return HttpResponseRedirect(url)


        form = BookForm()
        data = {"form":form}
        return render(request,"upload_csv.html", data)
    

admin.site.register(HomeBook)