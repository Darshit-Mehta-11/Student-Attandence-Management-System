from django.urls import path , include
from . import views

urlpatterns = [
    path('',views.home , name='home'),
    path('about',views.about , name='about'),
    path('contact',views.contact , name='contact'),
    path('change_password',views.change_pass , name='change_pass'),
]
