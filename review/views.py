import json

from .models import Review

from product.models import Product
from account.models import Account

from django.views  import View
from django.http   import HttpResponse , JsonResponse
from account.utils import login_check

class ReviewView(View):
    @login_check
    def post(self , request ,product_id):
        data    = json.loads(request.body)
        title   = data.get('title' , None)
        content = data.get('content',None)

        try :
            if Product.objects.filter(id = product_id).exists():
                if title and content:
                    Review(
                        title      = title ,
                        content    = content ,
                        user_id    = request.account.id,
                        product_id = product_id
                    ).save()

                    return HttpResponse(status=200)

        except Product.DoesNotExist:
            return JsonResponse({"message":"DOESNOT_PRODUCT"},status=400)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEY"} , status=400)

    @login_check
    def get(self , request):
        review_data = Review.objects.all().values()
        return JsonResponse({"data":list(review_data)} , status=200)

class ReviewDetailView(View):

    @login_check
    def post(self,request , product_id , review_id):
        data    = json.loads(request.body)
        title   = data.get("title" , None)
        content = data.get("content" , None)

        try :
            review_data = Review.objects.get(id         = review_id,
                                             product_id = product_id ,
                                             user_id    = request.account.id)

            if title and content:
                review_data.title   = title
                review_data.content = content
                review_data.save()

                return HttpResponse(status=200)

        except Review.DoesNotExist:
            return JsonResponse({"message":"DOESNOT_EXIST"} , status=400)

        except Account.DoesNotExist:
            return JsonResponse({"message":"DOESNOT_EXIST"} , status=400)

        except KeyError:
            return JsonResponse({"message":"INVALID_KEYS"} , status=400)

    @login_check
    def delete(self,request):
        return
