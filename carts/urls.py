from django.urls import path

from carts.views import CartView

urlpatterns = [
    path('/list', CartView.as_view()),
    path('/list/<int:user_id>', CartView.as_view()),
    path('/list/<int:cart_id>/delete', CartView.as_view()),
]