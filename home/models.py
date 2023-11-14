from django.db import models
from django.contrib.auth.models import User
from SystemSphereComputers.settings import MediaStorage


# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()
    overall_rating = models.IntegerField(default=1)
    item_pic = models.ImageField(upload_to='home/item_pics', storage=MediaStorage() ,blank=True)

    def __str__(self):
        return self.name


class UserProfileInfo(models.Model):
    # Create relationship (don't inherit from User!)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Add any additional attributes you want
    portfolio_site = models.URLField(blank=True)
    # pip install pillow to use this!
    # Optional: pip install pillow --global-option="build_ext" --global-option="--disable-jpeg"
    profile_pic = models.ImageField(upload_to='home/profile_pics', blank=True)

    def __str__(self):
        # Built-in attribute of django.contrib.auth.models.User !
        return self.user.username
