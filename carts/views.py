import json

from django.http.response import JsonResponse
from django.views         import View

from users.models    import User
from carts.models    import Cart
from products.models import Product, ProductOption, Size

class CartView(View):
    @decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = User.objects.get(id=1)
            product_id = data['product_id']
            size_id    = data['size_id']
            quantity   = data['quantity']
            
            if not ProductOption.objects.filter(product_id=product_id, size_id=size_id).exists():
                return JsonResponse({'message': 'ProductOption_DoesNotExist'}, status=404)
            
            product_option = ProductOption.objects.get(product_id=product_id, size_id=size_id)
                
            if quantity < 1 or quantity > int(product_option.stock):
                return JsonResponse({'message': 'INVALID_QUANTITY'}, status=400)
            
            cart, is_created = Cart.objects.get_or_create(
                user           = user,
                product_option = product_option,
                defaults       = {'quantity': 1}
            )

            cart.quantity = quantity
            cart.save()

            return JsonResponse({'message': 'SUCCESS'}, status=201)
            
        except KeyError:
            return JsonResponse({'message': 'KeyError'}, status=400)
        
    @decorator
    def get(self, request, user_id):
        user   = request.user
        carts  = Cart.objects.filter(user_id=user.id)
        result = []
        
        for cart in carts:
            product = cart.products_options.product
            images  = product.productimage_set.all()
            
            result.append(
                {
                    'product_id'    : product.id,
                    'product_name'  : product.name,
                    'product_number': product.product_number,
                    'price'         : int(product.price),
                    'size'          : cart.products_options.size.name,
                    'image_url'     : [image.url for image in images],
                    'quantity'      : cart.quantity
                }
            )
        return JsonResponse({'resutl': result}, status=200)
    
    def delete()