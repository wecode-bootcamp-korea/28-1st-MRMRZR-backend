from django.urls import path
from products.views import ProductDetailView

urlpatterns = [
    path('/detail', ProductDetailView.as_view()),
]
