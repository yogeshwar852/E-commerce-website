from . import views

from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('blogpost/<int:id>', views.blogpost, name="blogPost"),
]
