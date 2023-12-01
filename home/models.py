from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage
from django.db.models.signals import post_save
from django.dispatch import receiver

class MyStorage(S3Boto3Storage):
    bucket_name = 'system-sphere-bucket'


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name


# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()
    overall_rating = models.IntegerField(default=1)
    item_pic = models.ImageField(storage=MyStorage() ,blank=True)
    on_sale = models.BooleanField(default=False)
    available_online = models.BooleanField(default=False)
    price = models.FloatField()

    def __str__(self):
        return self.name
        
		
		
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)
		
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.available_online == False:
				shipping = True
		return shipping

	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total 

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total 
		
		

class OrderItem(models.Model):
	product = models.ForeignKey(Items, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total
		
		
class ShippingAddress(models.Model):
	customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address
		
		
# Signal to create Customer instance when User is created
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


# Signal to save Customer instance when User is saved
@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    instance.customer.save()