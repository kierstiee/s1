from django.db import models, transaction
from django.conf import settings
from django.forms.models import model_to_dict
from polymorphic.models import PolymorphicModel
from decimal import Decimal
from datetime import datetime
import stripe


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


    def image_urls(self):
        """Returns list of all images of a product"""
        # if no image return [image_unavailable.gif]
        p1 = Product(self)
        url = []
        if not p1.images.all():
            url.append(settings.STATIC_URL + 'catalog/media/products/image_unavailable.gif')
        else:
            for pi in p1.images.all():
                url.append(settings.STATIC_URL + 'catalog/media/products/' + pi.filename)
        return url

    def image_url(self):
        """Returns first image of product"""
        p1 = Product(self)
        # if no image return notfound.jpg
        if not p1.images.all():
            url = settings.STATIC_URL + 'catalog/media/products/image_unavailable.gif'
        else:
            url = Product.image_urls(p1.id)[0]
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


class Order(models.Model):
    '''An order in the system'''
    STATUS_CHOICES = (
        ( 'cart', 'Shopping Cart' ),
        ( 'payment', 'Payment Processing' ),
        ( 'sold', 'Finalized Sale' ),
    )
    order_date = models.DateTimeField(null=True, blank=True)
    name = models.TextField(blank=True, default="Shopping Cart")
    status = models.TextField(choices=STATUS_CHOICES, default='cart', db_index=True)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    user = models.ForeignKey('account.User', related_name='orders',  on_delete=models.CASCADE)
    # shipping information
    ship_date = models.DateTimeField(null=True, blank=True)
    ship_tracking = models.TextField(null=True, blank=True)
    ship_name = models.TextField(null=True, blank=True)
    ship_address = models.TextField(null=True, blank=True)
    ship_city = models.TextField(null=True, blank=True)
    ship_state = models.TextField(null=True, blank=True)
    ship_zip_code = models.TextField(null=True, blank=True)

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'Order {}: {}: {}'.format(self.id, self.user.get_full_name(), self.total_price)

    def active_items(self, include_tax_item=True):
        """Returns the active items on this order"""
        # create a query object (filter to status='active')
        items = []
        for item in OrderItem.objects.filter(order=self, status='active'):
            if item.product.name != 'Tax Item':
                items.append(item)
                if include_tax_item:
                    items.append(item)
        if items is not None:
            return items
        else:
            return 0

    def get_item(self, product, create=False):
        '''Returns the OrderItem object for the given product'''
        item = OrderItem.objects.filter(self, product).first()
        if item is None and create:
            item = OrderItem.objects.create(order=self, product=product, price=product.price, quantity=0)
        elif create and item.status != 'active':
            item.status = 'active'
            item.quantity = 0
        if item is not None:
            item.recalculate()
            item.save()
        item.recalculate(item)
        item.save()
        return item

    def num_items(self):
        '''Returns the number of items in the cart'''
        return sum(self.active_items(include_tax_item=False).values_list('quantity', flat=True))

    def recalculate(self):
        """
        Recalculates the total price of the order, including recalculating the taxable amount.
        Saves this Order and all child OrderLine objects.
        """

        # iterate the order items (not including tax item) and get the total price
        items = self.active_items(include_tax_item=False)
        # call recalculate on each item
        price = []
        for item in items:
            price.append(OrderItem.recalculate(item))
        # update/create the tax order item (calculate at 7% rate)
        total_price = 0
        for ind in price:
            total_price = total_price + ind
        tax = total_price * 0.07
        # update the total and save
        self.total_price = total_price + tax
        self.save()

    def finalize(self, stripe_charge_token):
        '''Runs the payment and finalizes the sale'''
        with transaction.atomic():

            # recalculate just to be sure everything is updated
            self.recalculate()
            # check that all products are available
            for item in self.active_items(include_tax_item=False):
                new_item = self.get_item(item)
                if new_item.quantity > item.product.quantity:
                    raise ValueError('There are not enough products to fulfil this order.')
            # contact stripe and run the payment (using the stripe_charge_token)

            # finalize (or create) one or more payment objects

            # set order status to sold and save the order

            # update product quantities for BulkProducts
            # update status for IndividualProducts


class OrderItem(PolymorphicModel):
    '''A line item on an order'''
    STATUS_CHOICES = (
        ( 'active', 'Active' ),
        ( 'deleted', 'Deleted' ),
    )
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    status = models.TextField(choices=STATUS_CHOICES, default='active', db_index=True)
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99
    quantity = models.IntegerField(default=0)
    extended = models.DecimalField(max_digits=8, decimal_places=2, default=0) # max number is 999,999.99

    def __str__(self):
        '''Prints for debugging purposes'''
        return 'OrderItem {}: {}: {}'.format(self.id, self.product.name, self.extended)


    def recalculate(self, item):
        '''Updates the order item's price, quantity, extended'''
        # update the price if it isn't already set and we have a product
        item_price = item.price
        item_quan = item.quantity
        # default the quantity to 1 if we don't have a quantity set
        if item_quan is None:
            item_quan = 1
        # calculate the extended (price * quantity)
        self.extended = item_quan * item_price
        # save the changes
        self.save()


class Payment(models.Model):
    '''A payment on a sale'''
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(null=True, blank=True)
    amount = models.DecimalField(blank=True, null=True, max_digits=8, decimal_places=2) # max number is 999,999.99
    validation_code = models.TextField(null=True, blank=True)
