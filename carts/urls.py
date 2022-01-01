from django.urls import path

from carts.views import CartView

urlpatterns = [
    path('/list', CartView.as_view()),
]