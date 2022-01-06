from django.urls import path

from products.views import ProductListView, ProductDetailView

urlpatterns = [
    path('', ProductListView.as_view()),
    path('/detail/<int:product_id>', ProductDetailView.as_view()),
]