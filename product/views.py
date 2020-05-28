from  django.views     import View
from  django.http      import HttpResponse, JsonResponse

from .models           import Product

class ProductView(View):
    def get(self , request , category_name):

        try :
            sort_by = request.GET.get('sort_by' , 'id')
            offset  = int(request.GET.get('offset' , 0))
            limit   = int(request.GET.get('limit' , 50))

            product_info = (Product.
                            objects.
                            filter(category__name__icontains = category_name).
                            order_by(sort_by).
                            values()[offset:offset+limit])

            return JsonResponse({"data":list(product_info)} , status=200)

        except ValueError:
            return JsonResponse({"message":"VALUDE_ERROR"} , status=400)

        except TypeError:
            return JsonResponse({"message":"INVALID_TYPE"} , status=400)

class ProductDetailView(View):
    def get(self , request ,category_name, product_id):

        try:

            product_info =(Product.
                           objects.
                           filter(id=product_id , category__name__icontains = category_name).
                           values())

            return JsonResponse({"data" : list(product_info)} , status=200)

        except TypeError:
            return JsonResponse({"MESSAGE" : "INVALID_TYPE"} , status=400)

        except Product.DoesNotExist:
            return JsonResponse({"MESSAGE" : "DOESNOT_PRODUCT"} , status=400)

        except Exception as e :
            return JsonResponse({"MESSAGE" : e} , status=400)

class SearchView(View):
    def get(self , request):
        print(123123)
        keyword = request.GET.get('keyword' , None)
        print(keyword)
        try :
            if len(keyword) > 0 :
                product_data = Product.objects.filter(name__icontains = keyword).values()

                return JsonResponse({"data" : list(product_data)},status=200)

        except ValueError:
            return HttpResponse(status=400)

        except TypeError:
            return HttpResponse(status=400)

        except Exception as e:
            return JsonResponse({"MESSAGE":e} , status=400)
