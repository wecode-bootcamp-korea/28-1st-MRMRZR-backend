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