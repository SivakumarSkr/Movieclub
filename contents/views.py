from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from contents.models import Blog, Answer, Review


# Create your views here.

class BlogListView(ListView):
    model = Blog
    paginate_by = 20
