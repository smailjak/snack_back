import jwt, bcrypt, json

from  django.db        import IntegrityError
from  django.db.models import Count, Q , Sum
from  django.views     import View
from  django.http      import HttpResponse, JsonResponse

from .models           import (Category,
                               Product,
                               CategoryProduct)

class CategoryView(View):
    def get(self , request):
        data = Category.objects.values()
        return JsonResponse({"data" : list(data)} , status=200)

class ProductView(View):
    def get(self , request , category_name):

        try :
            sort_by = request.GET.get('sort_by' , 'id')
            offset  = int(request.GET.get('offset' , 0))
            limit   = int(request.GET.get('limit' , 50))

            product_info = (Product.
                            objects.
                            filter(Q(category_name = category_name)).
                            order_by(sort_by).
                            values('id',
                                   'name',
                                   'image',
                                   'retail_price',
                                  )[offset:offset+limit])

            return JsonResponse({"data":list(product_info)} , status=200)

        except ValueError:
            return JsonResponse({"MESSAGE":"VALUDE_ERROR"} , status=400)

        except TypeError:
            return JsonResponse({"MESSAGE":"INVALID_TYPE"} , status=400)

class ProductDetailView(View):
    def get(self , request , product_id):

        try:
            data = (Product.
                    object.
                    filter(id = product_id).
                    values())

            return JsonResponse({"data" : list(data)} , status=200)

        except TypeError:
            return JsonResponse({"MESSAGE" : "INVALID_TYPE"} , status=400)

        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_PRODUCT"} , status=400)

        except Exception as e :
            return JsonResponse({"MESSAGE" : e} , status=400)

class SearchView(View):
    def get(self , request):
        keyword = request.GET.get("keyword" , None)
        try :
            if len(keyword) > 0:
                product_data = (Product.
                                objects.
                                filter(name = keyword).
                                values())

                return JsonResponse({"data" : product_data},status=200)

        except ValueError:
            return HttpResponse(status=400)

        except NoneType:
            return HttpResponse(status=400)

        except Exception as e:
            return JsonResponse({"MESSAGE":e} , status=400)
