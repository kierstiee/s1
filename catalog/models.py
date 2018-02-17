from django.db import models
from polymorphic.models import PolymorphicModel


class Category(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    name = models.TextField()
    description = models.TextField()


class Product(PolymorphicModel):

    TYPE_CHOICES = (
        (BULK, 'Bulk Product'),
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
    quantity = models.IntegerField(default=1)
    # image = models.ImageField()
    name = models.TextField()
    description = models.TextField()

    status = models.TextField(choices=STATUS_CHOICES,default='A')


class BulkProduct(Product):
    TITLE = 'Bulk'
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()


class IndividualProduct(Product):
    TITLE = 'Individual'
    itemID = models.TextField()


class RentalProduct(Product):
    TITLE = 'Rental'
    itemID = models.TextField()
    retire_date = models.DateTimeField(null=True, blank=True)
    max_rental_days = models.IntegerField(default=0)
