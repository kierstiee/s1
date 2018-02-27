from django.db import models
from polymorphic.models import PolymorphicModel
import os
from django.conf import settings


class Category(models.Model):
    name = models.TextField()
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


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

    name = models.TextField()
    description = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField(default=1)

    status = models.TextField(choices=STATUS_CHOICES,default='A')


class BulkProduct(Product):
    TITLE = 'BulkProduct'
    reorder_trigger = models.IntegerField()
    reorder_quantity = models.IntegerField()


class IndividualProduct(Product):
    TITLE = 'IndividualProduct'
    itemID = models.TextField()


class RentalProduct(Product):
    TITLE = 'RentalProduct'
    itemID = models.TextField()
    retire_date = models.DateField(null=True, blank=True)
    max_rental_days = models.IntegerField(default=0)


class ProductImage(models.Model):
    filename = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)

    def image_url(self):
        """Returns single image"""
        # if no image return notfound.jpg
        url = settings.STATIC_URL

    def image_urls(self):
        """Returns list of images"""
        # if no image return [notfound.jpg]

