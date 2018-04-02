from django.db import models
from cuser.models import AbstractCUser
from catalog import models as cmod


class User(AbstractCUser):
    birthdate = models.DateTimeField(null=True)
    address = models.TextField(null=True, blank=True)
    city = models.TextField(null=True, blank=True)
    state = models.TextField(null=True, blank=True)
    zipcode = models.TextField(null=True, blank=True)

    def get_purchases(self):
        return ['Roku Unlimited', 'Skis', 'Computer']

    def get_shopping_cart(self):
        order = cmod.Order.objects.filter(user=self, status='cart').first()
        if order is None:
            order = cmod.Order.objects.create(user=self, status='cart')
        return order
