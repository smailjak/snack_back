from django.core.validators import MinValueValidator , MaxValueValidator
from django.db              import models
from account.models         import Account
from product.models         import Product

# Create your models here.
class Basket(models.Model):
    account   = models.ForeignKey('account.Account' , on_delete = models.CASCADE , null=True)
    product   = models.ForeignKey('product.Product' , on_delete = models.CASCADE , null = True)
    quantity  = models.PositiveSmallIntegerField(null=True ,
                                                  default = 1 ,
                                                  validators=[MinValueValidator(1) ,
                                                              MaxValueValidator(30)])
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'baskets'

    def sub_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return self.product.name

class WishProduct(models.Model):
    account    = models.ForeignKey('account.Account' , on_delete = models.CASCADE , null = True)
    product    = models.ForeignKey('product.Product' , on_delete = models.CASCADE , null = True)
    created_at = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'wish_products'

class Order(models.Model):
    account       = models.ForeignKey('account.Account' , on_delete = models.CASCADE , null = True)
    created_at    = models.DateField(auto_now_add = True)
    is_closed     = models.BooleanField(default = False)
    class Meta:
        db_table = 'orders'

class OrderProduct(models.Model):
    order        = models.ForeignKey('Order'           , on_delete = models.SET_NULL , null = True)
    product      = models.ForeignKey('product.Product' , on_delete = models.CASCADE  , null = True)
    order_amount = models.PositiveSmallIntegerField(null       = True ,
                                                     default    = 1 ,
                                                     validators = [MinValueValidator(1) ,
                                                                   MaxValueValidator(30)])

    class Meta:
        db_table = "order_products"

