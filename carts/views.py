import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View

from carts.models    import Cart
from products.models import ProductOption

class CartView(View):
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            product_id = data['product_id']
            size_id    = data['size_id']
            quantity   = data['quantity']    # 값 추가할 경우 프론트에서 계산 후에 준 값으로 계산
            
            if not ProductOption.objects.filter(product_id=product_id, size_id=size_id).exists():
                return JsonResponse({'ProductOption_DoesNotExist'}, status=404)
            
            product_option = ProductOption.objects.get(product_id=product_id, size_id=size_id)
            
            if quantity < 1 or quantity > int(product_option.stock):
                return JsonResponse({'message': 'INVALID_QUANTITY'}, status=400)

            cart, is_created     = Cart.objects.get_or_create(
                user             = user,
                products_options = product_option,
                defaults         = {'quantity': 1}
            )
            cart.quantity = quantity
            cart.save()
            
            return JsonResponse({'message': 'SUCCESS'}, status=201)   
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)

    # @login_decorator    
    def get(self, request):
        user   = request.user
        carts  = Cart.objects.filter(user=user)
        result = []
        
        for cart in carts:
            product = cart.products_options.product
            image   = product.productimage_set.filter().first()
            
            result.append(
                {
                    'cart_id'       : cart.id,
                    'product_id'    : product.id,
                    'product_name'  : product.name,
                    'product_number': product.product_number,
                    'price'         : int(product.price),
                    'size'          : cart.products_options.size.name,
                    'image_url'     : image.url,
                    'quantity'      : cart.quantity
                }
            )
        return JsonResponse({'resutl': result}, status=200)

    # @login_decorator
    def delete(self, request, cart_id):
        user = request.user
        cart = Cart.objects.get(pk=cart_id)
        cart.delete()
        return JsonResponse({'message': 'NO_CONTENT'}, status=204)
