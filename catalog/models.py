from django.db import models
from polymorphic.models import PolymorphicModel


class Category(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    name = models.TextField()
    description = models.TextField()


class Product(PolymorphicModel):
    TYPE_CHOICES = (
        ('BulkProduct', 'Bulk Product'),
        ('IndividualProduct', 'Individual Product'),
        ('RentalProduct', 'Rental Product'),
    )
    STATUS_CHOICES = (
        ('A', 'Active'),
        ('I', 'Inactive'),
    )

    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    # image = models.ImageField()
    name = models.TextField()
    description = models.TextField()

    status = models.TextField(choices=STATUS_CHOICES,default='A')


class BulkProduct(Product):

    quantity = models.IntegerField()
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()


class IndividualProduct(Product):
    itemID = models.TextField()


class RentalProduct(Product):
    itemID = models.TextField()
    retire_date = models.DateTimeField()
    max_rental = models.IntegerField()
