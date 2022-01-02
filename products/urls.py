from django.urls import path
from products.views import ProductDetailView

urlpatterns = [
    #path('/detail', ProductDetailView.as_view()), 이렇게 url 짰을 땐 왜 안뜨나? 질문!
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
]