from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import (View, TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView)
from . import awslib
from .models import Items
from .forms import ItemsForm
import random
from django.utils.text import slugify
import os


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = Items.objects.all()
        context['items'] = items
        rating = []
        for i in items:
            rating.append(i.overall_rating)
        rating = {item.name: list(range(random.randint(0, 5))) for item in items}
        context['rating'] = rating
        print(len(rating))
        return context


class ItemCreateView(CreateView):
    model = Items
    form_class = ItemsForm
    template_name = 'home/add_product.html'
    success_url = reverse_lazy("home:index")

    def form_valid(self, form):
        # Use get method to access the 'image' key with a default value of None
        image = self.request.FILES.get('item_pic', None)
        print(image)

        if image:
            image_name = image.name
            new_filename = "test"
            # Get the file extension
            file_extension = os.path.splitext(image_name)[1]
            # Combine the new filename and original extension
            new_file_name_with_extension = f"{new_filename}{file_extension}"
            # Assign the new filename to the file object
            image.name = new_file_name_with_extension
            form.instance.item_pic = image
            # Additional processing or saving the form

            return super().form_valid(form)
        else:
            return HttpResponseBadRequest("No 'image' file submitted")
