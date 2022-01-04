import json

from django.http  import JsonResponse
from django.views import View

from products.models import Product

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id = product_id).exists():
            return JsonResponse({'message' : 'DOES NOT EXIST'}, status=404)
        
        product = Product.objects.get(id = product_id)
        images  = [image.url for image in product.productimage_set.all()]
        sizes   = [{'size_id' : size.id, 'size_name' : size.name} for size in product.sizes.all()]
        
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