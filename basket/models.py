from django.core.validators import MinValueValidator , MaxValueValidator
from django.db              import models
from account.models         import Account
from product.models         import Product

# Create your models here.
class Basket(models.Model):
    user         = models.ForeignKey('account.Account', on_delete = models.SET_NULL,  null=True)
    product      = models.ForeignKey('product.Product', on_delete = models.CASCADE, null = True)
    quantity     = models.PositiveSmallIntegerField(null=True ,
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
    user         = models.ForeignKey('account.Account' , on_delete = models.SET_NULL, null= True)
    product      = models.ForeignKey('product.Product' , on_delete = models.CASCADE, null = True)
    created_at   = models.DateTimeField(auto_now_add = True)

    class Meta:
        db_table = 'wish_products'



