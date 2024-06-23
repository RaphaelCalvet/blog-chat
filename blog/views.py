from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, UpdateView, DeleteView

from blog.forms import NewUserForm, BlogPostForm
from blog.models import BlogPost


class BlogPostListView(FormView, ListView):
    model = BlogPost
    template_name = 'blog/home.html'
    form_class = BlogPostForm
    context_object_name = 'posts'
    ordering = ['-pub_date']

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/post_edit.html'
    fields = ['title', 'content']
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        post = get_object_or_404(BlogPost, id=self.kwargs.get('pk'))
        if post.author != self.request.user:
            raise Http404()
        return post


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        post = get_object_or_404(BlogPost, id=self.kwargs.get('pk'))
        if post.author != self.request.user:
            raise Http404()
        return post


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registro bem sucedido.")
            return redirect("home")
        messages.error(request, "Ocorreu um erro durante o registro.")
    form = NewUserForm()
    return render(request=request, template_name="registration/register.html", context={"register_form": form})

def logout_view(request):
    logout(request)
    return redirect('/blog/login')
