from django.db import models
from polymorphic.models import PolymorphicModel


class Category(models.Model):
    create_date = models.DateTimeField.auto_now_add
    edit_date = models.DateTimeField.auto_now
    name = models.CharField()
    description = models.TextField()


class Product(PolymorphicModel):
    TYPE_CHOICES = (
        ('BulkProduct', 'Bulk Product'),
        ('IndividualProduct', 'Individual Product'),
        ('RentalProduct', 'Rental Product'),
    )
    CHOICES = (
        ('A', 'Active')
        ('I', 'Inactive')
    )

    create_date = models.DateTimeField.auto_now_add
    edit_date = models.DateTimeField.auto_now
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    numbers = models.IntegerField()
    image = models.ImageField()
    name = models.CharField()
    description = models.TextField()

    status = models.CharField(
        max_length=8,
        choices=CHOICES,
        default='A'
    )


class BulkProduct(Product):

    quantity = models.IntegerField()
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()


class IndividualProduct(Product):
    itemID = models.IntegerField()


class RentalProduct(Product):
    itemID = models.IntegerField()
    retire_date = models.DateTimeField()
    max_rental = models.IntegerField()
