import json

from django.http            import JsonResponse
from django.views           import View

from .models import Category, Item, Product, Size, ProductImage, ProductOption

class ProductListView(View):
    def get(self, request):
        categories     = Category.objects.all()
        items          = Item.objects.all()
        products       = Product.objects.all()
        sizes          = Size.objects.all()
        productimages  = ProductImage.objects.all()
        productoptions = ProductOption.objects.all()
        result         = []

        for category in categories:
            result.append(
                {
                    "category_name" : category.name
                }
            )
        for item in items:
            result.append(
                {
                    "item_name" : item.name
                }
            )
        for product in products:
            result.append(
                {
                    "product_name"             : product.name,
                    "product_number"      : product.product_number,
                    "product_description" : product.description,
                    "product_price"       : product.price,
                    "product_is_new"      : product.is_new,
                }
            )
        for size in sizes:
            result.append(
                {
                    "size_name" : size.name
                }
            )
        for productimage in productimages:
            result.append(
                {
                    "productimage_url" : productimage.url
                }
            )
        for productoption in productoptions:
            result.append(
                {
                    "stock" : productoption.stock
                }
            )
        return JsonResponse ({"result" : result }, status=200)