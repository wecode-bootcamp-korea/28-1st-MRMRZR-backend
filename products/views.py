import json

from django.http                    import JsonResponse
from django.views                   import View
from django.db.models.query_utils   import Q

from products.models import Category, Item, Product, Size, ProductImage, ProductOption

class ProductListView(View):
    def get(self, request):
        category     = request.GET.get('category', None)
        item          = request.GET.get('item', None)
        product       = request.GET.get('product', None)
        size          = request.GET.get('size', None)
        productimages  = request.GET.get('productimage', None)
        productoptions = request.GET.get('productoption', None)

        q = Q()

        if category:
            q &= Q(item__category__name=category)

        if item:
            q &= Q(item__name=item)

        # if pick:
        #     q &= Q(item__category__name=pick)

        products = Product.objects.filter(q)

        # if new:
        #     products = products.order_by('-created_at')[:4]

        result = [{
                    'id'           : product.id,
                    'name'         : product.name,
                    'description'  : product.description,
                    # 'price'        : int(product.get_price()
                    # 'image_url'    : [product_image.image_url for product_image in product.productimage_set.all()],
        } for product in products]
        return JsonResponse({'result': result}, status=200)
        # if category:
        #     q &= Q()



# class ProductDetailView(View):
#     def get(self, request):
#         try:
#             products = Product.objects.filter(items__id = item_id)
#             item = Item.objects.get(id = item_id)

#             result = [{
                
#             }]







        # categories     = Category.objects.all()
        # items          = Item.objects.all()
        # products       = Product.objects.all()
        # sizes          = Size.objects.all()
        # productimages  = ProductImage.objects.all()
        # productoptions = ProductOption.objects.all()
        # result         = []

        # for category in categories:
        #     result.append(
        #         {
        #             "category_name" : category.name
        #         }
        #     )
        # for item in items:
        #     result.append(
        #         {
        #             "item_name" : item.name
        #         }
        #     )
        # for product in products:
        #     result.append(
        #         {
        #             "product_name"             : product.name,
        #             "product_number"      : product.product_number,
        #             "product_description" : product.description,
        #             "product_price"       : product.price,
        #             "product_is_new"      : product.is_new,
        #         }
        #     )
        # for size in sizes:
        #     result.append(
        #         {
        #             "size_name" : size.name
        #         }
        #     )
        # for productimage in productimages:
        #     result.append(
        #         {
        #             "productimage_url" : productimage.url
        #         }
        #     )
        # for productoption in productoptions:
        #     result.append(
        #         {
        #             "stock" : productoption.stock
        #         }
        #     )
        # return JsonResponse ({"result" : result }, status=200)