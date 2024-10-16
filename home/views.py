from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.views.generic import (View, TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView)
from . import awslib
from .models import Items , Order, OrderItem, ShippingAddress, Customer, Store
from .forms import ItemsForm, UserSignupForm
import random
from django.utils.text import slugify
import os
from .utils import cookieCart, cartData, guestOrder
from django.http import JsonResponse
import json
import stripe
from django.conf import settings
from datetime import datetime
from . retailInvoiceGenerator import InvoiceGenerator




# This view renders the product catalog page
class IndexView(TemplateView):
    template_name = 'home/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Items.objects.all()
        data = cartData(self.request)
        cartItems = data['cartItems']
        check_retailer=self.request.user.is_authenticated and self.request.user.groups.filter(name='Retailer').exists()
        context = {'items': items, 'cartItems': cartItems, "is_retailer": check_retailer }
        rating = []
        for i in items:
            rating.append(i.overall_rating)
        rating = {item.name: list(range(random.randint(0, 5))) for item in items}
        context['rating'] = rating
        return context
        
        
        
# This view renders the product creation page
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Items
    item_id=Items.objects.order_by('-id').first().id
    value=f"https://system-sphere-bucket.s3.amazonaws.com/item{item_id}.jpg"
    form_class = ItemsForm
    form_class.base_fields['image_url'].initial = value
    template_name = 'home/add_product.html'
    success_url = reverse_lazy("home:index")

    def form_valid(self, form):
        # Use get method to access the 'image' key with a default value of None
        image = self.request.FILES.get('item_pic', None)
        print(image)

        if image:
            image_name = image.name
            new_filename = "item"
            item_id=Items.objects.order_by('-id').first().id
            new_file_name_with_extension = f"{new_filename}{item_id}.jpg"
            image.name = new_file_name_with_extension
            form.instance.item_pic = image

            return super().form_valid(form)
        else:
            return HttpResponseBadRequest("No 'image' file submitted")
            

# This view renders the stores list page
class StoreListView(View):
    template_name = 'home/store_list.html'

    def get(self, request, *args, **kwargs):
        stores = Store.objects.all()
        context = {'stores': stores}
        return render(request, self.template_name, context)



# This view renders the product update page
class ItemUpdateView(LoginRequiredMixin, UpdateView):
    model = Items
    form_class = ItemsForm  
    template_name = 'home/update_item.html'
    success_url = reverse_lazy("home:index")

    def form_valid(self, form):
        id = self.kwargs.get('pk')
        return super().form_valid(form)
        
        
# This view renders the product delete page
class ItemDeleteView(LoginRequiredMixin, DeleteView):
    model = Items
    template_name = 'home/delete_item.html'
    success_url = reverse_lazy("home:index")


# This view renders the signup page
class SignUpView(CreateView):
    template_name = 'home/signup.html'
    form_class = UserSignupForm
    success_url = reverse_lazy('home:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Subscribe user's email to SNS
        email_address = form.cleaned_data['email']
        print(email_address)
        awslib.subscribe_email_to_sns(email_address)

        return response
    

# This view renders the cart page
class CartView(View):
    def get(self, request, *args, **kwargs):
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        context = {'items': items, 'order': order, 'cartItems': cartItems}
        return render(request, 'home/cart.html', context)


# This view renders the checkout page
class CheckoutView(LoginRequiredMixin, View):
    template_name = 'home/checkout.html'

    def get(self, request, *args, **kwargs):
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        context = {'items': items, 'order': order, 'cartItems': cartItems, 'stripe_public_key': stripe_public_key}
        return render(request, self.template_name, context)


# This view renders the update cart item page
class UpdateItemView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        productId = data['productId']
        action = data['action']
        print('Action:', action)
        print('Product:', productId)

        customer = request.user.customer
        product = Items.objects.get(id=productId)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

        if action == 'add':
            orderItem.quantity = (orderItem.quantity + 1)
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)

        orderItem.save()

        if orderItem.quantity <= 0:
            orderItem.delete()

        return JsonResponse('Item was added', safe=False)


# This view renders the order processing page
class ProcessOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        transaction_id = str(datetime.now().timestamp()).replace('.','')
        data = json.loads(request.body)

        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
        else:
            customer, order = guestOrder(request, data)

        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )

        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
        
        item_list = []
        print(items)
        for i in range(0,len(items)):
           new_item = {'name': items[i]['product']['name'],'quantity': items[i]['quantity'], 'price': items[i]['product']['price']}
           item_list.append(new_item)
        
        username = request.user.username
    
        invoice_data = {
          'customer_name': username,
          'items': item_list,
          'transaction_id': transaction_id,
          'total': total,
          'order_date': str(datetime.now().date())
         }
         
        #Generating invoice and storing it to amazon s3
        invoice_generator = InvoiceGenerator(**invoice_data)
        invoice_generator.generate_invoice()
        s3_file_key=transaction_id+".pdf"
        invoice_generator.upload_to_s3(settings.AWS_STORAGE_BUCKET_NAME,s3_file_key)
        
        #sending transaction and invoice link to customer via SNS
        invoice_link="https://system-sphere-bucket.s3.amazonaws.com/"+s3_file_key
        subject = 'System Sphere Computers Order'
        message= f'You Order number {transaction_id} with amount {total} from System Sphere Computers is Successful.\nDownload Invoice at: {invoice_link}'
        email=username = request.user.email
        awslib.send_email_sns(subject, message, email)
        
        return JsonResponse('Payment submitted..', safe=False)
    