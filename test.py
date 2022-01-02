import json

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q
from django.core.exceptions import ValidationError

from products.models        import Category, Product, ThemeProduct, Theme, Material, ProductImage, ProductOption, Size, Color, ProductSet
from users.models           import Like, User
from core.utils             import signin_check_decorator, signin_decorator

class ProductView(View):
    @signin_check_decorator
    def get(self, request, product_id):
        try:
            product          = Product.objects.get(id=product_id)
            theme_ids        = list(product.themes.values_list("id", flat=True))
            related_products = Product.objects.filter(themes__id__in=theme_ids)
            is_liked         = Like.objects.filter(user=request.user, product=product_id).exists()
            
            result = {
                "id"                   : product.id,
                "name"                 : product.name,
                "price"                : product.price,
                "information"          : product.information,
                "keyword"              : product.keyword,
                "category"             : product.category.name,
                "is_liked"             : is_liked,
                "material_names"       : [material.name for material in product.material_set.all()],
                "material_cautions"    : [material.caution for material in product.material_set.all()],
                "images"               : [{"url" : image.url, "alt" : image.alt } for image in product.productimage_set.all()],
                "product_options"      : [{
                    "size"             : option.size.name,
                    "size_information" : option.size.information,
                    "stock"            : option.stock
                } for option in product.productoption_set.all()],
                "related_products"     : [{
                    "id"               : product.id,
                    "name"             : product.name,
                    "price"            : product.price,
                    "image_urls"       : [image.url for image in product.productimage_set.all()]
                }for product in related_products]
            }

            return JsonResponse({'result':result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'massage':"DoesNotExist"}, status=401)

class SetProductView(View):
    @signin_check_decorator
    def get(self, request, product_id):
        try:
            product        = Product.objects.get(id=product_id)
            is_liked       = Like.objects.filter(user=request.user, product=product_id).exists()
            
            result = {
                "id"          : product.id,
                "name"        : product.name,
                "price"       : product.price,
                "information" : product.information,
                "keyword"     : product.keyword,
                "category"    : product.category.name,
                "is_liked"    : is_liked,
                "images"      : [{"url" : image.url, "alt" : image.alt} for image in product.productimage_set.all()],
                "sub_products": [{
                    "id"    : product.product.id,
                    "name"  : product.product.name,
                    "price" : product.product.price,
                    "size"  : product.product.productoption_set.all()[0].size.name,
                    "color" : product.product.productoption_set.all()[0].color.name,
                    "images": [{
                        "url": image.url,
                        "alt": image.alt
                    }for image in product.product.productimage_set.all()]
                } for product in ProductSet.objects.filter(product_set=product)]
            }

            return JsonResponse({'result':result}, status=200)

        except Product.DoesNotExist:
            return JsonResponse({'massage':"DoesNotExist"}, status=401)

class ProductSetListView(View):
    def get(self, request):
        list_item   = []
        offset      = int(request.GET.get('offset', 0))
        limit       = int(request.GET.get('limit', 100))
        category_id = int(request.GET.get('categoryId',8))
        order       = request.GET.get('order', 'id')
        items       = Product.objects.select_related('category')\
                                    .filter(category=category_id).order_by(order)[offset:limit]
        
        if limit > 100:
            return JsonResponse({'MESSAGE':'LIMIT_ERROR'}, status = 400)

        for item in items: 
            product_items = ProductSet.objects.filter(product_set = item)
            list_item.append(
                {
                    'set_id'   : item.id,
                    'set_image': item.productimage_set.all()[0].url,
                    'set_alt'  : item.productimage_set.all()[0].alt,
                    'set_item' : [
                        {
                            'id'        : product_item.product.id,
                            'name'      : product_item.product.name,
                            'keyword'   : product_item.product.keyword,
                            'price'     : product_item.product.price,
                            'x_position': product_item.x_position,
                            'y_position': product_item.y_position,
                            'item_alt'  : product_item.product.productimage_set.all()[0].alt
                    } 
                    for product_item in product_items
                    ]
                }
            )
        return JsonResponse({'list_item': list_item}, status = 200)

class ProductListView(View):
    def get(self, request):
        offset      = int(request.GET.get('offset', 0))
        limit       = int(request.GET.get('limit', 100))
        theme_id    = int(request.GET.get("themeId", None)) if request.GET.get("themeId", None) != None else None
        category_id = int(request.GET.get("categoryId", None)) if request.GET.get("categoryId", None) != None else None
        ordering    = str(request.GET.get('ordering','created_at'))
        is_new      = request.GET.get('isNew',False)
        is_popular  = request.GET.get('isPopular', False)

        q = Q()

        if is_new:
            q &= Q(is_new = True)

        if is_popular:
            q &= Q(is_popular = True)

        if limit > 100:
            return JsonResponse({'MESSAGE':'LIMIT_ERROR'}, status = 400)

        if theme_id:
            q &= Q(themes = theme_id)

        if category_id:
            q &= Q(category__id = category_id)

        products    = Product.objects.select_related('category').prefetch_related('productimage_set','themes').filter(q).order_by(ordering)
        total_count = products.count()
        results     = [{
            'id'   : product.id,
            'name' : product.name,
            'price': product.price,
            'image': product.productimage_set.all()[0].url,
            'alt'  : product.productimage_set.all()[0].alt
        } for product in products[offset:limit]]

        return JsonResponse({'results' : results, 'total_count': total_count}, status =200)

class LikeView(View):
    @signin_decorator
    def post(self, request, product_id):
        try:
            like, is_like = Like.objects.get_or_create(product_id=product_id, user_id=request.user.id)
            
            if not is_like: 
                like.delete()
            
            return JsonResponse({'massage':"ToggleSuccess"}, status=200)
                
        except Product.DoesNotExist:
            return JsonResponse({'massage':"DoesNotExist"}, status=401)