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
            product = Product.objects.get(id=data['product_id'])    # id와 name 중에 name이 더 직관적이지만 우리가 데이터를 일일이 볼게 아니기도 하고 id가 조금이라도 메모리 공간?을 덜 잡아먹어서 id로 값을 보내는걸까?
            size = Size.objects.get(id=data['size_id'])
            quantity = data['quantity']
            
            # print('user : ', user)
            
            if not Product.objects.filter(id=product.id).exists():
                return JsonResponse({'message': 'INVALID_PRODUCT'}, status=400)
            
            if not Size.objects.filter(id=size.id).exists():
                return JsonResponse({'message': 'INVALID_SIZE'}, status=400)
            
            product_option = ProductOption.objects.filter(product_id=product, size_id=size)

            # print('productoption : ', product_option[0].id)

            # print('productoption[0] - stock : ', product_option[0].stock)

            if not quantity >= 1 or quantity <= int(product_option[0].stock):
                return JsonResponse({'message': 'INVALID_QUANTITY'}, status=400)

            if Cart.objects.filter(user_id=user).exists():
                cart = Cart.objects.create(
                    quantity = quantity
                )
                cart.quantity += quantity
                cart.save()
                return JsonResponse({'result': 'SUCCESS'}, status=201)
            
            cart = Cart.objects.create(
                user_id = user,
                products_options = product_option[0],
                quantity = quantity
            )
            #cart.quantity += quantity
            cart.save()
            return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
