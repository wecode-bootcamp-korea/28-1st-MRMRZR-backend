# Generated by Django 4.0 on 2022-01-09 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_product_sizes'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(through='products.ProductOption', to='products.Size'),
        ),
    ]
