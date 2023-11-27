from django.db import models
from django.contrib.auth.models import User
from storages.backends.s3boto3 import S3Boto3Storage

class MyStorage(S3Boto3Storage):
    bucket_name = 'system-sphere-bucket'

# Create your models here.
class Items(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    image_url = models.URLField()
    overall_rating = models.IntegerField(default=1)
    item_pic = models.ImageField(storage=MyStorage() ,blank=True)

    def __str__(self):
        return self.name
