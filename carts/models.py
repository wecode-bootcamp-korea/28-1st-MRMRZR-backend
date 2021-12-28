from django.db import models

from products.models import Product
from users.models    import User


class Cart(models.Model):
    user_id          = models.OneToOneField(User, on_delete=models.CASCADE)
    products_options = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity         = models.IntegerField()

    class Meta:
        db_table = 'carts'
