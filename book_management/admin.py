from django.contrib import admin

from .models import Book, Author, Genre, Comments

# Register your models here.

class BooksAdmin(admin.ModelAdmin):
    list_display = ["title", "author"]
    prepopulated_fields = {"slug":["title"]}
    list_filter = ["title", "author", "publication_date"]
    

class AuthorAdmin(admin.ModelAdmin):
    prepopulated_fields = {"full_name":["first_name","last_name"]}


class CommentsAdmin(admin.ModelAdmin):
    list_display = ["book"]
    list_filter = ["book"]

admin.site.register(Book, BooksAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Genre)
admin.site.register(Comments, CommentsAdmin)