from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic import ListView

from blog.forms import NewUserForm
from blog.models import BlogPost


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-pub_date']


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro bem sucedido.")
            return redirect("main:homepage")
        messages.error(request, "Ocorreu um erro durante o registro.")
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})