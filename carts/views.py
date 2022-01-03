import json

from django.http.response import JsonResponse
from django.views         import View

from users.models    import User
from carts.models    import Cart
from products.models import Product, ProductOption, Size

class CartView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            #user = request.user    유저에게 토큰 전달한것 인증되면 활성화해서 테스트
            user = User.objects.get(id=data['user_id'])
            product = Product.objects.get(id=data['product_id'])
            size = Size.objects.get(id=data['size_id'])
            quantity = data['quantity']
            
            if not Product.objects.filter(id=product.id).exists():
                return JsonResponse({'message': 'INVALID_PRODUCT'}, status=400)
            
            if not Size.objects.filter(id=size.id).exists():
                return JsonResponse({'message': 'INVALID_SIZE'}, status=400)
            
            product_option = ProductOption.objects.filter(product_id=product, size_id=size)
            print(product_option[0].stock)
            print(quantity)
            
            if quantity < 1 or quantity > int(product_option[0].stock):
                return JsonResponse({'message': 'INVALID_QUANTITY'}, status=400)

            if Cart.objects.filter(products_options=product_option).exists():       # get_or_create 참고 Product 테이블에 sizes라는 MTMF throug = ProductOption 
                Cart.objects.create(
                    products_options = product_option,
                    quantity = quantity,
                )
                return JsonResponse({'message': 'SUCESS ADD'}, status=201)
            else:
                
                cart = Cart.objects.create(
                    user_id = user,
                    products_options = product_option[0],
                    quantity = quantity
                )
                print(cart.quantity)
                cart.save()
                return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'DoesNotExist'}, status=401)

    def get(self, request, product_id):
        user = User.objects.get(id=product_id)