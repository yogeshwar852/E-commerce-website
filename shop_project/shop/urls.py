from . import views

from django.urls import path

urlpatterns = [
    path('', views.index, name="index"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('tracker/', views.tracker, name="rackingstatus"),
    path('search/', views.search, name="search"),
    path('products/<int:id>', views.products, name="products"),
    path('checkout/', views.checkout, name="checkout"),
    # path('handlerequest/', views.handlerequest, name="handlerequest"),
]
