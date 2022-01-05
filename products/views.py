import json

from django.http  import JsonResponse
from django.views import View

from products.models import Product, ProductOption

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id = product_id).exists():
            return JsonResponse({'message' : 'DOES NOT EXIST'}, status=404)
        
        product = Product.objects.get(id = product_id)
        images  = [{'image_id' : product_image.id, 'image_url' : product_image.url} for product_image in product.productimage_set.all()]
        sizes   = [{
            'size_id' : option.size.id, 
            'size_name' : option.size.name,
            'size_stock' : option.stock} for option in product.productoption_set.all()]
        
        result = {
            'id'             : product.id,
            'name'           : product.name,
            'product_number' : product.product_number,
            'description'    : product.description,
            'price'          : int(product.price),
            'is_new'         : product.is_new,
            'image_urls'     : images,
            'sizes'          : sizes
        }               
            
        return JsonResponse({'results' : result}, status = 200)

class ProductListView(View):
    def get(self, request):
        try:
            category = request.GET.get('category', None)
            item     = request.GET.get('item', None)
            size     = request.GET.getlist('size', None)
            sort     = request.GET.get('sort', "id")
            offset   = int(request.GET.get('offset', 0))
            limit    = int(request.GET.get('limit', 8))

            q = Q(productoption__stock__gt=0)

            if category:
                q &= Q(item__category__name=category)

            if item:
                q &= Q(item__name=item)

            if size:
                q &= Q(sizes__in=size)

            sort_set = {
                "id"               : "id",
                "price_ascending"  : "price",
                "price_descending" : "-price"
            }

            results = [{
                'product_id'    : product.id,
                'name'          : product.name,
                'product_number': product.product_number,
                'price'         : int(product.price),
                'is_new'        : product.is_new,
                'item'          : product.item.name,
                "image"         : [image.url for image in product.productimage_set.all()]
            } for product in Product.objects.filter(q).distinct().order_by(sort_set[sort])[offset:offset+limit]
            ]
            return JsonResponse({"results" : results}, status = 200)