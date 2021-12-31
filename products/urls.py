from django import path
from products.views import ProductDetailView

urlpatterns = [
    path('/product_detail', ProductDetailView.as_view())
]
