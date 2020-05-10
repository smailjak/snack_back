import json
from django.test import TestCase , Client

from .models     import (Category,
                         Product,
                         CategoryProduct)

class CategoryViewTest(TestCase):

    def setUp(self):
        Category.objects.bulk_create([
            Category(id=1 , name="과자"),
            Category(id=2 , name="음료"),
            Category(id=3 , name="초콜릿"),
            Category(id=4 , name="수입과자"),
        ])


    def tearDown(self):
        Category.objects.all().delete()

    def test_get_category(self):
        client   = Client()
        response = client.get('/product')

        self.assertEqual(
            response.json(),
            {"data": [
                {
                    "id"   : 1 ,
                    "name" : "과자",
                },
                {
                    "id"   : 2,
                    "name" : "음료",
                },
                {
                    "id"   : 3,
                    "name" : "초콜릿",
                },
                {
                    "id"   : 4,
                    "name" : "수입과자",
                }
            ]}
        )
        self.assertEqual(response.status_code, 200)

class ProductViewTest(TestCase):

    def setUp(self):

        Category.objects.create(
            id   = 1 ,
            name = "과자",
        )

        Product.objects.create(
            id           = 1,
            name         = "빼빼로" ,
            image        = "빼빼로 이미지" ,
            price        = "100" ,
            retail_price = "200",
        )

        CategoryProduct.objects.create(
            id       = 1,
            category_id = Category.objects.get(id=1).id,
            product_id  = Product.objects.get(id=1).id,
        )
    def tearDown(self):
        Category.objects.all().delete()
        Product.objects.all().delete()
        CategoryProduct.objects.all().delete()

    def test_get_product(self):
        client     = Client()
        response   = client.get("/product/과자", {"offset" : 0 , "limit" : 50})

        self.assertEqual(response.json(),
            {
                "data" :[
                {
                    "id"           : 1 ,
                    "name"         : "빼빼로",
                    "image"        : "빼빼로 이미지" ,
                    "price"        : "100",
                    "retail_price" : "200",
                }
            ]
            }
        )

        self.assertEqual(response.status_code, 200)

class ProductDetailViewTest(TestCase):

    def setUp(self):
        client = Client()

        Product.objects.create(
            id           = 1,
            name         = "빼빼로" ,
            image        = "빼빼로 이미지" ,
            price        = "100" ,
            retail_price = "200",
        )

    def tearDown(self):
        Product.objects.all().delete()

    def test_get_product_detail(self):
        client   = Client()
        response = client.get("/product/1/detail")

        self.assertEqual(response.json(),
            {
                "data" :[
                {
                    "id":1,
                    "name":"빼빼로",
                    "image":"빼빼로 이미지",
                    "price":"100",
                    "retail_price":"200",
                    "ingredient_image":None,
                    "stock":None
                }
            ]
            }
        )

        self.assertEqual(response.status_code, 200)

