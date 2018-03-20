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


    def image_url(self):
        """Returns first image of product"""
        p1 = Product(self)
        # if no image return notfound.jpg
        if not p1.images.all():
            url = settings.STATIC_URL + 'catalog/media/products/image_unavailable.gif'
        else:
            for pi in p1.images.all():
                url = settings.STATIC_URL + 'catalog/media/products/' + pi.filename
        return url

    def image_urls(self):
        """Returns list of all images of a product"""
        # if no image return [notfound.jpg]
        p1 = Product(self)
        url = []
        if not p1.images.all():
            url = settings.STATIC_URL + 'catalog/media/products/image_unavailable.gif'
        else:
            for pi in p1.images.all():
                for fn in pi.filename:
                    url.append(settings.STATIC_URL + 'catalog/media/products/' + fn + '.jpg')
        return url

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
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    filename = models.TextField()

# NOT_FOUND_PRODUCT_IMAGE = ProductImage()
