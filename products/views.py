import json

from django.http import JsonResponse
from django.views import View

from products.models import Category, Item, Product, Size, ProductImage, ProductOption

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id = product_id).exists():
            return JsonResponse({'message' : 'DOES NOT EXIST'}, status=404)
        
        product = Product.objects.get(id = product_id)
        
        # images = []

        # for image in product.productimage_set.all():
        #     images.append(image.url)

        images = [image.url for image in product.productimage_set.all()]
        
        
        sizes = []

        for size in product.sizes.all():
            sizes.append(
                {
                    'size_id'   : size.id,
                    'size_name' : size.name
                }
            )
        
        result = {
            'id'             : product.id,
            'name'           : product.name,
            'product_number' : product.product_number,
            'description'    : product.description,
            'price'          : product.price,
            'is_new'         : product.is_new,
            'image_urls'     : images,
            'sizes'         : sizes
        }               
            
        return JsonResponse({'results' : result}, status = 200)
        
        
            #image = ProductImage.objects.get(product_id = product_id) # 질문
            #size = Size.objects.get(size_id = product_id) # 질문
            # 딕셔너리 만들기 전 지정해주어야 하는 요소들 방식 질문!
            # Product.objects.all() ???
            #image = product.image_set.all()
            #size = product.size_set.all()
            #image = ProductImage.objects.get(product_id = product_id) #이 부분 질문 - url을 꺼내온다?
            # 이미지 클래스에서 불러오기
            
            # get 과 filter의 차이 (개수, 방식 등등)