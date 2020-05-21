import json

from django.views           import View
from django.http            import HttpResponse, JsonResponse

from .models                import Account
from product.models         import Product
from basket.models          import Basket , WishProduct
from account.utils          import login_check


class BasketView(View):
    @login_check
    def post(self , request):
        data = json.loads(request.body)

        product = Product.objects.filter(id=data['product_id'], is_in_stock=True)

        if not product.exists():
            return JsonResponse({'message': 'OUT_OF_STOCK'}, status=200)

        try :
            if Basket.objects.filter(user_id    = request.user.id ,
                                     product_id = data['product_id']).exists():

                basket_data = Basket.objects.get(product_id = data['product_id'] ,
                                                 user_id    = request.user.id)

                basket_data.update(quantity=data['quantity'])
                basket_data.save()

            else:
                Basket(
                    user_id    = request.account.id,
                    product_id = data['product_id'],
                    quantity   = data['quantity']
                ).save()

            return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({'message' : 'INVALID_KEY'} , status=400)

        except Account.DoesNotExist:
            return JsonResponse({'message' : 'DOESNOT_ACCOUNT'},status=400)

        except Product.DoesNotExist:
            return JsonResponse({'message' : 'DOESNOT_PRODUCT'}, status=400)

    @login_check
    def get(self, request):

        try:
            basket_data = Basket.objects.filter(user_id=request.user_id).select_related('product')

            data = []

            for basket in basket_data:
                basket_list = {
                    "id"           : basket.product.id,
                    "image"        : basket.product.image,
                    "name"         : basket.product.name,
                    "price"        : basket.product.price,
                    "retail_price" : basket.product.retail_price,
                }

                data.append(basket_list)

            return JsonResponse({'data': list(data)}, status=200)

        except Basket.DoesNotExist:
            return JsonResponse({'message' :'DOESNOT_BASKET'}, status=400)

        except Account.DoesNotExist:
            return JsonResponse({'message' :'DOESNOT_ACCOUNT'},status=400)

    @login_check
    def delete(self, request):
        data   = json.loads(request.body)
        basket = Basket.objects.filter(user_id=request.user.id , product_id=data['product_id'])

        if basket.exists():
            basket.get().delete()

            return HttpResponse(status=200)

        return JsonResponse({'message': 'INVALID_INPUT'}, status=400)

class WishProductView(View):
    @login_check
    def post(self , request):
        data    = json.loads(request.body)
        product = Product.objects.filter(id=data['product_id'])

        try :
            if WishProduct.objects.filter(product_id = data['product_id']).exists():
                return JsonResponse({"message" : "이미추가된 아이템"} ,status=400)


            WishProduct(
                user_id    = request.account.id,
                product_id = data['product_id'],
            ).save()

            return HttpResponse(status=200)

        except:
            return JsonResponse({"message": "doesnot_product"}, status=400)

    @login_check
    def get(self , request):
        try :

            wish_product = WishProduct.objects.filter(user_id = request.user.id).select_related('product')
            data = []

            for wish in wish_product:
                wish_list = {
                    "id"           : wish.product.id,
                    "image"        : wish.product.image,
                    "name"         : wish.product.name,
                    "price"        : wish.product.price,
                    "retail_price" : wish.product_retail_price
                }
                data.append(wish_list)

        except WishProduct.DoesNotExists:
            return JsonResponse({'message' : 'DOESNOT_WISHPRODUCT'},status=400)

        except ValueError:
            return JsonResponse({'message' : 'INVALID_ERROR'} , status=400)

    @login_check
    def delete(self, request):
        data         = json.loads(request.body)
        wish_product = WishProduct.objects.filter(user_id    = request.user.id ,
                                                  product_id = data['product_id'])
        try :

            if wish_product.exists():
                wish_product.get().delete()

                return HttpResponse(status=200)

        except KeyError:
            return JsonResponse({"message" : "INVALID_KEY"} , status=400)

        except Product.DoesNotExist:
            return JsonResponse({"message" : "DOESNOT_PRODUCT"} , status=400)
