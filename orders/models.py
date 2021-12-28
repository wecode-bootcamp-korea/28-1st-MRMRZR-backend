from django.db import models

from products.models import ProductOption
from users.models    import User

class OrderStatus(models.Model):
    status = models.CharField(max_length=20)

    class Meta:
        db_table = 'orders_status'
    
    
class Order(models.Model):
    order_number = models.CharField(max_length=20)
    user_id      = models.ForeignKey(User, on_delete=models.CASCADE)
    order_status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE)
    address      = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'orders'
        
class OrderItem(models.Model):
    products_options_id = models.ForeignKey(ProductOption, on_delete=models.CASCADE)
    quantity            = models.IntegerField()
    order_id            = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'orders_items'
