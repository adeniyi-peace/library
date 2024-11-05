from django.urls import path
from . import views

urlpatterns = [
    path("", views.WelcomeView.as_view(), name= "index"),
    path("register", views.RegisterView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("books", views.BookListView.as_view(), name="allbooks"),
    #path("filter", views.SearchView.as_view(), name="filter"),
    path("author/<int:pk>", views.AuthorDetailsView.as_view(), name="author_details"),
    path("books/<slug:slug>", views.BookDetailView.as_view(), name= "book_detail"),
    path("books/genre/<str:genre>", views.GenreListView.as_view(), name="genrelist"),
]
