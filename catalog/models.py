from django.db import models
# from polymorphic import


class Category(models):
    create_date = models.DateTimeField.auto_now_add
    edit_date = models.DateTimeField.auto_now
    name = models.TextField(null=True, blank=True)

class Product(models):
    create_date = models.DateTimeField.auto_now_add
    edit_date = models.DateTimeField.auto_now

    price = models.DecimalField(null=True, blank=True)
    status = models.TextField(null=True, blank=True)
