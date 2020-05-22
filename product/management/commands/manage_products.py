import csv
from pathlib import Path

from django.core.management.base import BaseCommand

from product.models import Category, Product

class Command(BaseCommand):
    help = 'manage product objects'

    def add_arguments(self, parser):
        parser.add_argument('--delete-all-products', action='store_true', dest='delete_all_products')
        parser.add_argument('--delete-all-category', action='store_true', dest='delete_all_category')

        parser.add_argument('--add-category', action='store_true', dest='add_category')
        parser.add_argument('--dump-products', action='store_true', dest='dump_products')

    def handle(self, *args, **options):
        if options['delete_all_products']:
            Product.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('deleted all'))
        
        if options['delete_all_category']:
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('deleted all category'))

        if options['add_category']:
            Category.objects.create(name = "snack")
            Category.objects.create(name = "gum")
            Category.objects.create(name = "ramen")
            Category.objects.create(name = "drink")
            Category.objects.create(name = "imported_snack")
            
            self.stdout.write(self.style.SUCCESS('Successfully added category '))


        if options['dump_products']:
            category_names = ['snack', 'gum', 'ramen', 'drink', 'imported_snack']
            for category_name in category_names:
                dump_file_path = Path(f'scrapings/{category_name}.csv')
                with open(dump_file_path, newline='') as csvfile:
                    smapreader = csv.reader(csvfile)
                    for row in smapreader:
                        Product.objects.create(
                            image = row[0],
                            name = row[1],
                            price_strike = row[2],
                            price_red = row[3],
                            item_price = row[4]
                        )
            
            self.stdout.write(self.style.SUCCESS('Successfully dumped products by category'))
