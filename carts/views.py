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
            user = User.objects.get(email=data['email'])
            product_name = data['product_name']
            size_name = data['size_name']
            quantity = data['quantity']
            
            print()
            print('user : ', user)
            print()
            
            if not Product.objects.filter(name=product_name).exists():
                return JsonResponse({'message': 'INVALID_PRODUCT'}, status=400)
            
            if not Size.objects.filter(name=size_name).exists():
                return JsonResponse({'message': 'INVALID_SIZE'}, status=400)
            
            product = Product.objects.get(name=product_name)
            size = Size.objects.get(name=size_name)
            
            productoption = ProductOption.objects.filter(product_id=product, size_id=size)

            print()
            print('productoption : ', productoption[0].id)
            print()
            
            print()
            print('productoption[0] - stock : ', productoption[0].stock)
            print()
            
            '''if User.objects.filter(email=data['email']).exists():
                Cart.objects.create(
                    products_options = productoption[0],
                    quantity = quantity
                )
                return JsonResponse({''})'''

            if quantity < 1 or quantity > int(productoption[0].stock):
                return JsonResponse({'message': 'INVALID_QUANTITY'}, status=400)


            
            cart = Cart.objects.create(
                user_id = user,
                products_options = productoption[0],
                quantity = quantity
            )
            #cart.quantity += quantity
            cart.save()
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
        