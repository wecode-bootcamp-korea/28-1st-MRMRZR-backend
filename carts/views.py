import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse
from django.views         import View

from users.models    import User
from carts.models    import Cart
from products.models import ProductOption

class CartView(View):
    def post(self, request):
        try:
            # user = request.user    유저에게 토큰 전달한것 인증되면 활성화해서 테스트
            data       = json.loads(request.body)
            user       = User.objects.get(id=1)
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
                
        # jsondecodeerror 수정    
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'message': 'JSONDecodeError'}, status=400)

    # @login_decorator    
    def get(self, request, user_id):
        user   = request.user
        #user  = User.objects.get(pk=user_id)
        carts  = Cart.objects.filter(user_id=user.id)
        result = []
        
        for cart in carts:
            product = cart.products_options.product
            image   = product.productimage_set.filter().first()
            
            result.append(
                {
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

# def delete 는 body가 없어서 path와 queryparameter 중에 선택해야 함