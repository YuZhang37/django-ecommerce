from django.db import models


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


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # .product_set to get all products with a single promotion
    # https://www.sankalpjonna.com/learn-django/the-right-way-to-use-a-manytomanyfield-in-django


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True)
    description = models.TextField()
    inventory = models.IntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    last_updated_at = models.DateTimeField(auto_now=True)

    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)


class Customer(models.Model):
    BRONZE = 'b'
    SILVER = 's'
    GOLD = 'g'
    MEMBERSHIP_CHOICES = [
        (BRONZE, 'bronze'),
        (SILVER, 'silver'),
        (GOLD, 'gold'),
    ]
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
