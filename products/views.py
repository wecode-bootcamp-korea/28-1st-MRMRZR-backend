import json

from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist

from products.models import Category, Item, Product, Size, ProductImage, ProductOption

class ProductDetailView(View):
    def get(self, request, product_id):
        try:
            if not Product.objects.filter(id = product_id).exists():
                return JsonResponse({'message' : 'DOES NOT EXIST'}, status=404)
            
            product = Product.objects.get(id = product_id)
            image = ProductImage.objects.get(product_id_id = product_id)
            
            #sizes = ProductOption.objects.filter(product_id_id = product_id)
            #size = ProductOption.objects.filter(product_id_id = product_id)
            #sizes = request.GET.get('size')
            
            result = {
                'id'             : product.id,
                'name'           : product.name,
                'product_number' : product.product_number,
                'description'    : product.description,
                'price'          : product.price,
                'is_new'         : product.is_new,
                'image_url'      : image.url
                #'size'           : Size 클래스 혹은 위에서 할당한 ProductOption 클래스?
                #'image_url' : [product.image_url for product in image],
            }               
                
            return JsonResponse({'results' : result}, status = 200)
        
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'NOT_FOUND'}, status=401)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=401)
        
        
            #image = ProductImage.objects.get(product_id = product_id) # 질문
            #size = Size.objects.get(size_id = product_id) # 질문
            # 딕셔너리 만들기 전 지정해주어야 하는 요소들 방식 질문!
            # Product.objects.all() ???
            #image = product.image_set.all()
            #size = product.size_set.all()
            #image = ProductImage.objects.get(product_id = product_id) #이 부분 질문 - url을 꺼내온다?
            # 이미지 클래스에서 불러오기
            
            # get 과 filter의 차이 (개수, 방식 등등)