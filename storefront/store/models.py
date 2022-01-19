import uuid
from decimal import Decimal

from django.contrib import admin
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings

# django automatically creates an id as the primary key, if the primary key is
# not specified.
from core.models import User


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        # tell django not to create the reverse relationship '+'
        related_query_name='featured_collection',
    )

    # type annotation
    def __str__(self) -> str:
        # return super().__str__()
        return self.title + ', ' + str(self.featured_product_id)

    class Meta:
        ordering = ['title']


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # .product_set to get all products with a single promotion
    # https://www.sankalpjonna.com/learn-django/the-right-way-to-use-a-manytomanyfield-in-django


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True)
    # null=True, only applies to the database
    # to make it optional in the admin interface: blank=True
    description = models.TextField(null=True, blank=True)
    inventory = models.IntegerField(
        validators=[MinValueValidator(1)],
    )
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)],
    )
    last_updated_at = models.DateTimeField(auto_now=True)

    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)

    # ManyToManyField
    # optional when creating a record, it would be an empty list if it's not set
    promotions = models.ManyToManyField(Promotion)

    def get_price_with_tax2(self):
        return self.unit_price * Decimal(1.2)

    def __str__(self) -> str:
        return self.name + ', ' + str(self.inventory)

    class Meta:
        ordering = ['name']


class Customer(models.Model):
    BRONZE = 'b'
    SILVER = 's'
    GOLD = 'g'
    MEMBERSHIP_CHOICES = [
        (BRONZE, 'bronze'),
        (SILVER, 'silver'),
        (GOLD, 'gold'),
    ]
    # each tuple:
    # first element- actual value stored in database
    # second element: human readable notes, which is also used in admin

    # first_name = models.CharField(max_length=255)
    # last_name = models.CharField(max_length=255)
    # email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=255)
    birthday = models.DateField(null=True)
    membership = models.CharField(
        max_length=1,
        choices=MEMBERSHIP_CHOICES,
        default=BRONZE
    )

    # a process to do this (I think):
    # 1. create all users from customers tables with customer_id
    # 2. add fields user with onetoonefield(null=true)
    # 3. populated user field with information from user table with customer_id
    # 4. alter user table, drop customer_id
    # 5. alter customer table, onetoonefield(null=false)
    # and drop first_name, last_name, email and indices

    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    # )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )

    # onetoonefield is not working well for migrations without null=True, need to supply a user
    # migrations: the index is dropped,
    # the reverse process of creating it is not succeeded
    class Meta:
        # not support for creating index on the attributes of referring objects.
        # indexes = [
        #     models.Index(fields=('user__last_name', 'user__first_name')),
        #     models.Index(fields=('user__email',)),
        #     models.Index(fields=('phone_number',))
        # ]
        ordering = ('user__first_name', 'user__last_name')
        permissions = [
            ('view_history', 'Can view history')
        ]

    def __str__(self) -> str:
        return f'{self.user.last_name} {self.user.first_name}'

    # first_name can be sorted in admin page
    # https://docs.djangoproject.com/en/4.0/ref/contrib/admin/
    # display controls how the field is displayed
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name

    # last_name can be sorted in admin page
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name


class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED = 'F'
    PAYMENT_CHOICES = [
        (PAYMENT_PENDING, 'pending'),
        (PAYMENT_COMPLETE, 'complete'),
        (PAYMENT_FAILED, 'failed'),
    ]
    placed_at = models.DateTimeField(auto_now=True)
    payment_status = models.CharField(
        max_length=1,
        choices=PAYMENT_CHOICES,
        default=PAYMENT_PENDING,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name='orders',
    )

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    # anonymous user can place cart
    # the primary id is an integer, easy to hack
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # quantity = models.SmallIntegerField()
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(1000), ]
    )

    class Meta:
        unique_together = [['cart', 'product'], ]


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    # customer = models.OneToOneField(
    #     # Customer class should be in front of the Address class,
    #     # Otherwise, we can use 'Customer'
    #     Customer,
    #     on_delete=models.CASCADE()
    # )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    # textfield has no limitation on the text
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

