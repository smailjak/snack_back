import csv

from pathlib                     import Path
from django.core.management.base import BaseCommand
from product.models              import (Category,
                                         Product)

'''
우선적으로 제가 스스로 코드좀 볼려고 코드들 마다 주석을 일단 달았습니다. ㅎㅎ
원래 작업하는 코드에 주석을 다는것을 별로 안좋아하지만..
공부가 끝나면 제가 주석다 지우겠습니다 감사합니다 ㅎㅎ
'''

class Command(BaseCommand):
    help = 'manage product objects'

    def add_arguments(self, parser):
        parser.add_argument('--delete-all-products' , action = 'store_true'  , dest = 'delete_all_products')
        parser.add_argument('--delete-all-category' , action = 'store_true'  , dest = 'delete_all_category')
        parser.add_argument('--add-category'        , action = 'store_true'  , dest = 'add_category')
        parser.add_argument('--dump-products'       , action = 'store_true'  , dest = 'dump_products')

    def handle(self, *args, **options):
        if options['delete_all_products']: # create 하기전 product all delete
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('deleted all'))

        if options['delete_all_category']: # create 하기전 category all delete
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('deleted all category'))

        if options['add_category']: # category create
            Category.objects.create(name = "snack")
            Category.objects.create(name = "gum")
            Category.objects.create(name = "ramen")
            Category.objects.create(name = "drink")
            Category.objects.create(name = "imported_snack")

            self.stdout.write(self.style.SUCCESS('Successfully added category '))

        if options['dump_products']:
            category_names = ['snack', 'gum', 'ramen', 'drink', 'imported_snack']
            for category_name in category_names: # snack 부터 하나씩 반복 돌림 
                dump_file_path = Path(f'scrapings/{category_name}.csv') # snack.csv 부터 하나씩 경로를 불러옴 
                with open(dump_file_path, newline='') as csvfile:
                    smapreader = csv.reader(csvfile) # csv 파일 열어준다 
                    for row in smapreader: # 반복문 돌림
                        Product.objects.create(
                            image        = row[0],
                            name         = row[1],
                            price_strike = row[2],
                            price_red    = row[3],
                            item_price   = row[4]
                        )
            
            self.stdout.write(self.style.SUCCESS('Successfully dumped products by category'))
