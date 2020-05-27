from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=250 , null=True)

    class Meta:
        db_table="categorys"

class Product(models.Model):
    name             = models.CharField(max_length=250)
    image            = models.CharField(max_length=500 , null=True)
    price_strike     = models.CharField(max_length=250, default=0)
    price_red        = models.CharField(max_length=250, default=0)
    item_price       = models.CharField(max_length=250, default=0)
    ingredient_image = models.CharField(max_length=500 , null=True)
    delivery_guide   = models.CharField(max_length=250 , null=True)
    stock            = models.IntegerField(null=True)
    created_at       = models.DateTimeField(auto_now_add=True , null=True)
    updated_at       = models.DateTimeField(auto_now=True , null=True)
    category         = models.ForeignKey('Category', on_delete=models.CASCADE, null=True)

    class Meta:
        db_table="products"

