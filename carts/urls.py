from django.urls import path

from carts.views import CartView

urlpatterns = [
    path('/cart', CartView.as_view()),
    path('/cart/<int:user_id>', CartView.as_view()),
]