import os
import csv
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mrmrzara.settings')
django.setup()

from products.models import Category, Item, Product, ProductImage, ProductOption, Size


CSV_PATH_PRODUCTS = '/home/bruno/workspace/mrmrzara/csv/mrmrzara.csv'
CSV_PATH_PRODUCTS_OPT = '/home/bruno/workspace/mrmrzara/csv/options.csv'
CSV_PATH_PRODUCTS_URL = '/home/bruno/workspace/mrmrzara/csv/url.csv'


def category():
    with open(CSV_PATH_PRODUCTS) as in_file:
        data = csv.reader(in_file)
        next(data, None)
        for row in data:
            if row[0]:
                name = row[0]
                Category.objects.create(name=name)
            
def item():
    with open(CSV_PATH_PRODUCTS) as in_file:
        data = csv.reader(in_file)
        next(data, None)
        for row in data:
            if row[0]:
                category_name = row[0]
            # 빈칸 없다는 가정하에 작성한 코드
            item_name = row[1]
            category  = Category.objects.get(name=category_name)
            #print(item_name, category_id)
            Item.objects.create(name=item_name, category=category)

def product():
    with open(CSV_PATH_PRODUCTS) as in_file:
        data = csv.reader(in_file)
        next(data, None)
        for row in data:
            if row[1]:
                item_name = row[1]
            
            name           = row[2].split(',')
            product_number = row[3].split(',')
            description    = row[4].split(',')
            price          = row[5].split(',')
            is_new         = row[6].split(',')
            item           = Item.objects.get(name=item_name)
            for i in range(len(name)):
                Product.objects.create(
                    name           = name[i],
                    product_number = product_number[i],
                    description    = description[i],
                    price          = price[i],
                    is_new         = is_new[i],
                    item           = item
                )

def options():  # ProductOption 데이터 입력
    with open(CSV_PATH_PRODUCTS_OPT) as in_file:
        data = csv.reader(in_file)
        next(data, None)
        for row in data:
            if row[0]:
                product = row[0]
            
            size    = row[1].split(',')
            stock   = row[2].split(',')
            product = Product.objects.get(id=product)
            for i in range(len(size)):
                size_name = Size.objects.get(name=size[i])
                ProductOption.objects.create(
                    product = product,
                    size    = size_name,
                    stock   = stock[i]
                )

def images():
    with open(CSV_PATH_PRODUCTS_URL) as file:
        data = csv.reader(file)
        next(data, None)
        for row in data:
            product_id = row[0]
            product    = Product.objects.get(id=product_id)
            url        = row[1].split(',')
            for i in range(len(url)):
                ProductImage.objects.create(
                    url     = url[i],
                    product = product
                )
  
# category()
# item()
# product()
# options()
# images()