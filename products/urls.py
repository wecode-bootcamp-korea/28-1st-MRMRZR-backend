from django.urls import path
from products.views import ProductDetailView

urlpatterns = [
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
]