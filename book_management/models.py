from typing import Iterable
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.text import slugify

# Create your models here.

class Genre(models.Model):
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.genre



class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(null=True, max_length=100)
    image = models.ImageField(upload_to="author profile", height_field=None, width_field=None, max_length=None)
    biography = models.TextField()
    DOB = models.DateField(max_length=50)
    nationality = models.CharField(max_length=50)
    genre = models.ManyToManyField(Genre, related_name="author")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def save(self, *args, **kwargs):
        self.full_name = f"{self.first_name} {self.last_name}"
        super().save(*args, **kwargs)
    


class Book(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(unique=True)
    cover_image = models.ImageField(upload_to="book cover", height_field=None, 
                                    width_field=None, max_length=None, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="book", null=True)
    publication_date = models.DateField(max_length=50, null=True)
    ISBN = models.CharField( max_length=20, null=True)
    description = models.TextField( null=True)
    page_count = models.IntegerField(validators=[MinValueValidator(1)], null=True)
    genre = models.ManyToManyField(Genre, related_name="book", )

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    

class Comments(models.Model):
    username = models.CharField(max_length=100)
    ratings = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user_review = models.TextField()
    date = models.DateField(auto_now=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="comments")



