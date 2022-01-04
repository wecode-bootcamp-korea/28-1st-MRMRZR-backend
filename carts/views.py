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
            
            product_option = ProductOption.objects.get(product_id=product, size_id=size)
            print(product_option)
            
            if quantity < 1 or quantity > int(product_option.stock):
                return JsonResponse({'message': 'INVALID_QUANTITY'}, status=400)

            if Cart.objects.filter(products_options__in=product_option).exists():       # get_or_create 참고
                cart = Cart.objects.create(
                    user_id = user.id,
                    products_options = product_option[0],
                    quantity = quantity,
                )
                cart.quantity += quantity
                cart.save()
                return JsonResponse({'message': 'SUCESS_CART_TO_ADD'}, status=201)
            
            else:
                print(user)
                cart = Cart.objects.create(
                    user_id = user.id,
                    products_options = product_option,
                    quantity = quantity
                )
                print(cart.quantity)
                cart.save()
                return JsonResponse({'message': 'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'DoesNotExist'}, status=401)

    def get(self, request, user_id):
        try:
            user  = User.objects.get(pk=user_id)
            carts = Cart.objects.filter(user_id=user.id)
            result = []
            for cart in carts:
                option = cart.products_options.product
                images = option.productimage_set.all()
                
                result.append(
                    {
                        'user_id'       : cart.user.id,
                        'product_name'  : option.name,
                        'product_number': option.product_number,
                        'price'         : int(option.price),
                        'size'          : cart.products_options.size.name,
                        'image_url'     : [image.url for image in images],
                        'quantity'      : cart.quantity
                    }
                )
            return JsonResponse({'resutl': result}, status=200)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User_DoesNotExist'}, status=404)
        except Cart.DoesNotExist:
            return JsonResponse({'message': 'Cart_DoesNotExist'}, status=404)