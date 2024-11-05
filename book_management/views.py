from typing import Any
from django.db.models import Q, Avg 
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, TemplateView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import auth
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator

from .models import Book, Genre, Author
from .forms import UserCreateForm, LoginForm, CommentForm

# Create your views here.

class WelcomeView(TemplateView):
    template_name= "book_management/index.html"


class RegisterView(View):
    def get(self, request):
        form = UserCreateForm()

        if request.user.is_authenticated:
            return redirect(reverse("index"))
        
        context = {"form":form, "login":False}
        return render(request, "book_management/login_page.html", context)

    def post(self, request):
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse("login"))
        
        context = {"form":form, "login":False}
        return render(request, "book_management/login_page.html", context)



class LoginView(View):
    def get(self, request):
        form = LoginForm()
        next = request.GET.get("next")


        if request.user.is_authenticated:
            return redirect(reverse("index"))

        context = {"form":form, "login":True, "next":next}
        return render(request, "book_management/login_page.html", context)
    
    def post(self, request):
        response = request.POST
        form = LoginForm(response)
        next = request.POST.get("next")

        if form.is_valid():
            username = response.get("username")
            password =response.get("password")
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)

                if next!="None":
                    return redirect(next)
                
                return redirect(reverse("index"))

        context = {"form":form, "login":True, "next":next}
        return render(request, "book_management/login_page.html", context)
    

class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        return redirect(reverse("index"))



class BookListView(ListView):
    paginate_by = 10
    model = Book
    template_name = "book_management/all_books.html"
    context_object_name = "books"
    ordering = "?"
    
    # to-do: put the search task into a new view
    # to prevent some-errors such as seeing nextpage for only one result
    # look up Filterview 
    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if search:=self.request.GET.get("search") :
            filter = Q(title__icontains=search)|Q(author__full_name__contains=search)
            books = self.model.objects.filter(filter)
            paginator, page, queryset, is_paginated = self.paginate_queryset(books, 10)
            context = {
                "paginator": paginator,
                "page_obj": page,
                "is_paginated": is_paginated,
                "books": queryset,
                "search": search
            }
            
        return context
    
# search view need only to copy get_contextdata from BookListView
# removing the if statement and using the listview class  for searchview  
# class SearchView(View):
#     def get(self, request):
#         search = request.GET.get("search")
#         model = get_object_or_404(Book)


class GenreListView(View):
    def get(self, request, genre):
        model =get_object_or_404( Genre, genre__iexact=genre).book.all()
        page   = Paginator(model, 10)

        page_number = request.GET.get("page")
        page_obj = page.get_page(page_number)
        
        context = {"books":page_obj.object_list, "page_obj":page_obj}
        return render(request, "book_management/all_books.html", context=context)


class BookDetailView(LoginRequiredMixin, DetailView, FormView):
    login_url = "/login"
    model = Book
    template_name = "book_management/book_detail.html"
    context_object_name = "book"
    form_class = CommentForm
    success_url = None

    def form_valid(self, form) -> HttpResponse:
        form = form.save(commit=False)
        form.username = self.request.user.username
        form.book = self.get_object()
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["genres"] = self.get_object().genre.all
        context["usercomment"] = self.get_object().comments.all()
        context["ratings"] = self.get_object().comments.all().aggregate(Avg("ratings"))
        context["author"] = self.get_object().author
        return context
    
    def get_success_url(self) -> str:
        return (reverse("book_detail", args=[self.kwargs.get(self.slug_url_kwarg)]))


class AuthorDetailsView(LoginRequiredMixin, View):
    login_url = "/login"
    
    def get(self, request, pk):
        model = get_object_or_404(Author, pk=pk)
        context = {
            "author":model,
            "books":model.book.all()
        }
        return render(request, "book_management/author_details.html", context)
