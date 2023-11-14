from django.contrib import admin
from django.urls import path
from home import views

# SET THE NAMESPACE!
app_name = 'home'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('addItem/', views.ItemCreateView.as_view(), name='add_item'),
]


