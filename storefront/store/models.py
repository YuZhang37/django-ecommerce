from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

# django automatically creates an id as the primary key, if the primary key is
# not specified.


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product',
        on_delete=models.SET_NULL,
        null=True,
        # tell django not to create the reverse relationship
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
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=255)
    birthday = models.DateField(null=True)
    membership = models.CharField(
        max_length=1,
        choices=MEMBERSHIP_CHOICES,
        default=BRONZE
    )

    class Meta:
        indexes = [
            models.Index(fields=('last_name', 'first_name')),
            models.Index(fields=('email',)),
            models.Index(fields=('phone_number',))
        ]
        ordering = ('first_name', 'last_name')

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name}'


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


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    # anonymous user can place cart
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField()


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

