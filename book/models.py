from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Book(models.Model):
    ISBN= models.CharField(max_length=20,null=True)
    english_name= models.CharField(max_length=100,null=True)
    nepali_name= models.CharField(max_length=100,null=True)
    slug = models.SlugField(max_length=500 , null=True,default='')
    genre= models.CharField(max_length=100,null=True)
    english_author= models.CharField(max_length=100,null=True)
    nepali_author=models.CharField(max_length=100,null=True)
    avg_rating=models.FloatField(null=True)
    Publisher= models.CharField(max_length=100,null=True)
    no_of_pages=models.IntegerField(null=True)
    year_published=models.CharField(max_length=40,null=True)
    image=models.URLField(null=True)

    def __str__(self):
        return self.english_name


class Review(models.Model):
    book = models.ForeignKey(Book , on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model() , on_delete=models.CASCADE)
    review_text = models.TextField()
    review= models.IntegerField(default=0)
    date_posted = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-date_posted']

    def __str__(self):
        return str(self.author) + ' comment on ' + self.book.english_name[:30]
    
    @property
    def date(self):
        return self.date_posted.strftime('%d %b, %Y').upper()


    
class Order(models.Model):
    user= models.ForeignKey(get_user_model() , on_delete=models.CASCADE)
    books= models.ManyToManyField(Book)
    def __str__(self):
        return self.user.username

class HomeBook(models.Model):
    book= models.ForeignKey(Book,on_delete=models.CASCADE)

    def __str__(self):
        return self.book.english_name