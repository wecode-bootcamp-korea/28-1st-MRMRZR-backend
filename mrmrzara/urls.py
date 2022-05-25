from django.urls import include, path


urlpatterns = [
    path('api/v1/products', include('apps.products.urls')),
    path('api/v1/users', include('apps.users.urls')),
    path('api/v1/carts', include('apps.carts.urls')),
]
