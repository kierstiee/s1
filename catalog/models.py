from django.db import models
# from polymorphic import


class Category(models.Model):
    create_date = models.DateTimeField.auto_now_add
    edit_date = models.DateTimeField.auto_now
    name = models.TextField(null=True, blank=True)

class Product(models.Model):
    create_date = models.DateTimeField.auto_now_add
    edit_date = models.DateTimeField.auto_now
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(null=True, blank=True)

    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    CHOICES = (
        (ACTIVE, 'Active')
        (INACTIVE, 'Inactive')
    )
    status = models.CharField(
        max_length=8,
        choices=CHOICES,
        default=ACTIVE
    )

class BulkProduct(Product):

class RentalProduct(Product):

class IndividualProduct(Product):
