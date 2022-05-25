from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = 'categories'


class Item(models.Model):
    name     = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'items'


class Size(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        db_table = 'sizes'


class Product(models.Model):
    name           = models.CharField(max_length=50)
    product_number = models.CharField(max_length=50)
    description    = models.TextField()
    price          = models.DecimalField(max_digits=10, decimal_places=2)
    is_new         = models.BooleanField(default=False)
    item           = models.ForeignKey(Item, on_delete=models.CASCADE)
    sizes          = models.ManyToManyField(Size, through='ProductOption')

    class Meta:
        db_table = 'products'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    url     = models.CharField(max_length=16000)

    class Meta:
        db_table = 'products_images'


class ProductOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size    = models.ForeignKey(Size, on_delete=models.CASCADE)
    stock   = models.IntegerField()

    class Meta:
        db_table = 'products_options'
