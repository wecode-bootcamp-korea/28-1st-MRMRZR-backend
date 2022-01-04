import json

from django.http                    import JsonResponse
from django.views                   import View
from django.db.models.query_utils   import Q

from products.models import Category, Item, Product, Size, ProductImage, ProductOption



# 이름, 가격, imgurl, size,
class ProductListView(View):
    def get(self, request):
        """
        1. 조건의 맞는 product list을 전달해 주는 것이 목적
        2. 조건이 무엇있는가
        => catrgory, item, size, 높은 가격순, 낮은 가격순, 페이지네이션

        """
        1. 프론트에서 온 값들 점검
        2. 가공이 필요한 로직
        3. 내가 응답할 데이터 

        
        category = request.GET.get('category', None)
        item     = request.GET.get('item', None)
        size     = request.GET.getlist('size', None) # => [X, L, XL]
        sort     = request.GET.get('sort', "id")
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 5))
        
        """
        size 쿼리 파라미터 2가지 방법
        1. :8000/products?item=abc&sort=price&size=X&size=L&size=XL
        => request.GET.getlist('size', None) # => [X, L, XL]
        
        2. :8000/products?item=abc&sort=price&size=X,L,XL
            request.GET.get('size', None) # => X,L,XL
            sizes = size.split(',') => X, L, XL]
        """
        
        q = Q(productoption__stock__gt=0)

        if category:
            q &= Q(item__category__name=category)
        
        if item:
            q &= Q(item__name=item)
        
        if size:
            q &= Q(sizes__in=size) #size는 list여야 한다.
            
        sort_set = {
            "id"     : "id",
            "price"  : "price",
            "-price" : "-price"
        }

        results = [{
            'product_id'    : product.id,
            'name'          : product.name,
            'product_number': product.product_number,
            'price'         : product.price,
            'is_new'        : product.is_new,
            'item'          : product.item.name,
            "image"         : product.productimage_set.first()
        } for product in Product.objects.filter(q).order_by(sort_set[sort])[offset:offset+limit]]
    
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