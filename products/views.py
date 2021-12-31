import json

from django.http import JsonResponse
from django.views import View
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from django.db.models import Sum, Q

from products.models import Category, Item, Product, Size, ProductImage, ProductOption


class ProductDetailView(View):
    def get(self, request):
        try:
            product_id = request.GET.get('id')
            product = Product.objects.get(id = product_id) 
            if not Product.objects.filter(id = product_id).exists():
                return JsonResponse({'message' : 'DOES NOT EXIST'}, status=404)
            
               
            # 딕셔너리 만들기 전 지정해주어야 하는 요소들 방식 질문!
            # Product.objects.all() ???
            #image = product.image_set.all()
            #size = product.size_set.all()
            #image = ProductImage.objects.get(product_id = product_id) #이 부분 질문 - url을 꺼내온다?
            # 이미지 클래스에서 불러오기
            #size = 
            
            result = {
                'id' : product.id,
                'name' : product.name,
                'product_number' : product.product_name,
                'description' : product.description,
                'price' : product.price,
                'is_new' : product.is_new,
                #'image_url' : [product.image_url for product in image],
                #'size' : size.name,
            }               
                
            return JsonResponse({'results' : result}, status = 200)
        
        except Product.DoesNotExist:
            return JsonResponse({'message' : 'NOT_FOUND'}, status=401)