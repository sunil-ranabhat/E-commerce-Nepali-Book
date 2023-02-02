from django.db import models

# Create your models here.
class Book(models.Model):
    ISBN= models.CharField(max_length=20,null=True)
    english_name= models.CharField(max_length=100,null=True)
    nepali_name= models.CharField(max_length=100,null=True)
    english_author= models.CharField(max_length=100,null=True)
    nepali_author=models.CharField(max_length=100,null=True)
    avg_rating=models.FloatField(null=True)
    Publisher= models.CharField(max_length=100,null=True)
    no_of_pages=models.IntegerField(null=True)
    year_published=models.CharField(max_length=40,null=True)
    image=models.ImageField(upload_to='images')

    def __str__(self):
        return self.english_name

