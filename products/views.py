import json

from django.http                    import JsonResponse
from django.views                   import View
from django.db.models.query_utils   import Q

from products.models import Category, Item, Product, Size, ProductImage, ProductOption



# 이름, 가격, imgurl, size,
class ProductListView(View):
    def get(self, request):
        try:
            if not Product.objects.filter(id = product_id).exsists():
                return JsonResponse({'message' : 'PRODUCT DOES NOT EXIST'}, status=404)
            
            product = Product.objects.get(id = product_id)
            image = ProductImage.objects.get(product_id_id = product_id)

            result = {
                'id'        : product.id,
                'name'      : product.name,
                'price'     : product.price,
                'is_new'    : product.is_new,
                'image_url' : image.url
            }
            
            return JsonResponse({"results" : results}, status = 200)


# sort = request.GET.get('sort')
# ...

# sort_set = {
#     'price_ascending'  : 'price',
#     'price_descending' : '-price',
# }
# ...

# ...filter(product_list).order_by(sort_set.get(sort, 'id'))