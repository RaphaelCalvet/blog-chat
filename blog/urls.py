from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import BlogPostListView, BlogPostUpdateView, BlogPostDeleteView

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('register/', views.register_request, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', BlogPostListView.as_view(), name='home'),
    path('post/<int:pk>/edit/', BlogPostUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', BlogPostDeleteView.as_view(), name='post_delete'),
]
