import json

from django.http                    import JsonResponse
from django.views                   import View
from django.db.models.query_utils   import Q

from products.models import Category, Item, Product, Size, ProductImage, ProductOption



# 이름, 가격, imgurl, size,
class ProductListView(View):
    def get(self, request):
        products = Product.objects.filter()
        images   = [image.url for image in product.productimage_set.all()]
        sizes    = [size.name for size in product.productoption_set.all()]
        order_condition = request.GET.get('order', None)

        if order_condition == 'price_ascending':
            products = Product.objects.order_by('price')

        if order_condition == 'price_descending':
            products = Product.objects.order_by('-price')

        products = [{
            'id'            : product.id,
            'name'          : product.name,
            'product_number': product.product_number,
            'price'         : product.price,
            'is_new'        : product.is_new,
            'item'          : product.item,
            "images"        : images,
            "sizes"         : sizes,
        } for product in products
        ]
        
        
        results = {
            'products' : products
        }

        return JsonResponse({"results" : results}, status = 200)

"""
order by ( 정렬 ) = 가격순

django queryset slicing 
& 
django orderby

14 filter 뒤 값들이 변경될것을 생각




2. limit, offset 
내가 정한 갯수만 (슬라이싱 사용) 보내주기?


3. 필터
"""









        # try:
        #     if not Product.objects.filter(id = product_id).exsists():
        #         return JsonResponse({'message' : 'PRODUCT DOES NOT EXIST'}, status=404)
            
        #     product = Product.objects.get(id = product_id)
        #     image = ProductImage.objects.get(product_id = product_id)

        #     result = {
        #         'id'        : product.id,
        #         'name'      : product.name,
        #         'price'     : product.price,
        #         'is_new'    : product.is_new,
        #         'image_url' : image.url
        #     }
            
        #     return JsonResponse({"results" : results}, status = 200)


# sort = request.GET.get('sort')
# ...

# sort_set = {
#     'price_ascending'  : 'price',
#     'price_descending' : '-price',
# }
# ...

# ...filter(product_list).order_by(sort_set.get(sort, 'id'))