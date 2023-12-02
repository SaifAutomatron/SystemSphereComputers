from django.contrib import admin
from django.urls import path, reverse_lazy, include
from home import views
from django.contrib.auth.views import LoginView, LogoutView

# SET THE NAMESPACE!
app_name = 'home'

# Be careful setting the name to just /login use userlogin instead!
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('addItem/', views.ItemCreateView.as_view(), name='add_item'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', LoginView.as_view(template_name='home/Login.html', success_url=reverse_lazy('home:index'),next_page='home:index'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home:index'), name='logout'),
	path('cart/', views.CartView.as_view(), name="cart"),
    path('checkout/', views.CheckoutView.as_view(), name="checkout"),
    path('update_item/', views.UpdateItemView.as_view(), name="update_item"),
    path('process_order/', views.ProcessOrderView.as_view(), name="process_order"),
    path('update/<int:pk>/', views.ItemUpdateView.as_view(), name='update_item'),
    path('delete/<int:pk>/', views.ItemDeleteView.as_view(), name='delete_item'),
    
]

