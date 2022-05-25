from django.db import models

from ..products.models import ProductOption
from ..users.models    import User


class Cart(models.Model):
    user             = models.ForeignKey(User, on_delete=models.CASCADE)
    products_options = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity         = models.IntegerField()

    class Meta:
        db_table = 'carts'
