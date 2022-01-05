from django.urls import include, path

urlpatterns = [
    path('products', include('products.urls')),
    path('users', include('users.urls')),
    path('products', include('products.urls'))
]
