from django.test import Client
from django.test import TestCase

from .models     import (Category,
                         Product,
                         CategoryProduct)


class ProductViewTest(TestCase):
    def setUp(self):
        category = Category.objects.create(
            {id : 1 , name : "과자"},
            {id : 2 , name : "음료"},
            {id : 3 , name : "초콜릿"},
            {id : 4 , name : "수입과자"},
        )

    def test_get_category_success(self):
        client  = Client()
        reponse = client.get('/product')
        self.assertEqual(response.json(),
                         {
                             'data': [{1 : "과자"},
                                      {2 : "음료"}]
                         }
                        )

        self.assertEqual(response.status_code, 200)

    def test_get_product_success(self):
        client     = Client()
        test_snack = [
            {id : 1 , name : "빼빼로"},
            {id : 2 , name : "꿈틀꿈틀"},
        ]
        response   = client.get("/product/과자")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json() , {"data" :test_snack})

    def test_get_product_detail_success(self):
        client   = Client()
        response = client.get("/product/1")
        self.assertEqual(response.status_code, 200)

        test_snack_detail = [
            {
                id           : 1 ,
                name         : "빼빼로" ,
                price        : "100" ,
                retail_price : "200" ,
                image        : "빼빼로 이미지"
            }
        ]

        self.assertEqual(response.json(), {"data" : test_snack_detail})

    def test_get_search_success(self):
        client   = Client()
        response = client.get("/product/search" , {"keyword" : "빼빼로"})
        self.assertEqual(response.status_code , 200)
        test_search = [
            {
                id           : 1 ,
                name         : "빼빼로" ,
                price        : "100" ,
                retail_price : "200" ,
                image        : "빼빼로 이미지",
            },
            {
                id           : 2 ,
                name         : "땅콩빼빼로" ,
                price        : "300" ,
                retail_price : "400" ,
                image        : "빼빼로 이미지2",
            }
        ]

        self.assertEqual(
            response.json(),
            {
                "data":list(test_search)
            }
        )
