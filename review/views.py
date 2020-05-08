from .models import Review

from product.models import Product
from account.models import Account

from django.views   import View
from django.http    import HttpResponse , JsonResponse

class ReviewView(View):
    def post(self , request):
        return
    def get(self , request):
        return

class ReviewDetailView(View):
    def post(self ,request):
        return
    def delete(self ,request):
        return

