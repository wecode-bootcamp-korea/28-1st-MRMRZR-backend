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
            # user = request.user    유저에게 토큰 전달한것 인증되면 활성화해서 테스트
            # user = get_object_or_404(User, user=request.user)
            user             = User.objects.get(pk=data['user_id'])
            product          = Product.objects.get(id=data['product_id'])
            size             = Size.objects.get(id=data['size_id'])
            product_quantity = data['quantity']
            product_option   = ProductOption.objects.get(product_id=product, size_id=size)
            
            if product_quantity < 1 or product_quantity > int(product_option.stock):
                return JsonResponse({'message': 'INVALID_QUANTITY'}, status=400)

            if Cart.objects.filter(user=user, products_options=product_option).exists():
                current_quantity = Cart.objects.get(user=user, products_options=product_option).quantity
                cart, is_created = Cart.objects.update_or_create(
                    user_id=user,
                    products_options_id=product_option,
                    defaults= {'quantity': int(product_quantity) + current_quantity}
                )
                return JsonResponse({'message': 'SUCCESS'}, status=201)
                
            else:
                # get_or_create 참고
                cart = Cart.objects.create(
                    user_id = user.id,
                    products_options = product_option,
                    quantity = product_quantity
                )
                return JsonResponse({'message': 'SUCCESS'}, status=201)
            
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message': 'User_DoesNotExist'}, status=401)
        except Product.DoesNotExist:
            return JsonResponse({'message': 'Product_DoesNotExist'}, status=401)
        except Size.DoesNotExist:
            return JsonResponse({'message': 'Size_DoesNotExist'}, status=401)
        except ProductOption.DoesNotExist:
            return JsonResponse({'message': 'ProductOption_DoesNotExist'}, status=401)
        
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
