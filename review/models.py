from django.db      import models
from account.models import *
from product.models import *


# Create your models here.

class Review(models.Model):
    user       = models.ForeignKey('Account' , on_delete=models.CASCADE)
    product    = models.ForeignKey('Product' , on_delete=models.CASCADE)
    title      = models.CharField(max_length=250)
    content    = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        db_table = "reviews"
