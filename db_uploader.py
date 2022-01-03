import os, django, csv, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mrmrzara.settings")
django.setup()

from products.models import Category, Item, Product, ProductImage, ProductOption, Size

CSV_PATH_PRODUCTS = '/Users/wonsukji/desktop/wecode/28-1st-MRMRZR-backend/mrmrzara-DB/products_DB.csv'

def category():
    with open(CSV_PATH_PRODUCTS) as in_file:
        data = csv.reader(in_file)
        next(data, None)
        for row in data:
            if row[0]:
                name = row[0]
                Category.objects.create(name = name)


def item():
    with open(CSV_PATH_PRODUCTS) as in_file:
        data = csv.reader(in_file)
        next(data, None)
        for row in data:
            if row[0]:
                category_name = row[0]
            item_name = row[1]
            category_id = Category.objects.get(name = category_name)
            Item.objects.create(name = item_name, category_id = category_id)

         
def product():
    with open(CSV_PATH_PRODUCTS) as in_file:
        data = csv.reader(in_file)
        next(data, None)
        for row in data:
            if row[1]:
                item_name = row[1]
                
            product_name = row[2].split(',')
            product_number = row[3].split(',')
            product_description = row[4].split(',')
            product_price = row[5].split(',')
            product_is_new = row[6].split(',')
            product_item_id = Item.objects.get(name = item_name)
                
            for i in range(len(product_name)):
                Product.objects.create(
                    name = product_name[i],
                    product_number = product_number[i],
                    description = product_description[i],
                    price = product_price[i],
                    is_new = product_is_new[i],
                    item_id = product_item_id
                )

CSV_PATH_PRODUCTS_OPT = '/Users/wonsukji/desktop/wecode/28-1st-MRMRZR-backend/mrmrzara-DB/options.csv'

def options():
    with open(CSV_PATH_PRODUCTS_OPT) as in_file:
        data = csv.reader(in_file)
        next(data, None)
        for row in data:
            if row[0]:
                product_id = row[0]
            
            size = row[1].split(',')
            stock = row[2].split(',')
            product_id = Product.objects.get(id = product_id)
            for i in range(len(size)):
                size_id = Size.objects.get(name = size[i])
                ProductOption.objects.create(
                    product_id = product_id,
                    size_id = size_id,
                    stock = stock[i]
                )

CSV_PATH_PRODUCTS_IMG = '/Users/wonsukji/desktop/wecode/28-1st-MRMRZR-backend/mrmrzara-DB/images.csv'

def images():
    with open(CSV_PATH_PRODUCTS_IMG) as in_file:
        data = csv.reader(in_file)
        next(data, None)
        for row in data:
            if row[0]:
                product_id = row[0]
            
            url = row[1].split(',')
            product_id = Product.objects.get(id = product_id)
            
            for i in range(len(url)):
                ProductImage.objects.create(
                    product_id = product_id,
                    url = url[i]
                )
        
#category()
#item()
#product()
#options()
#images()