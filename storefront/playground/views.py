from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Concat
from django.http import HttpResponse
from django.shortcuts import render
from store.models import Product, OrderItem, Order, Customer
from tags.models import Tag, TaggedItem
from django.db.models import (
    Q,
    F,
    aggregates,
    Value,
    IntegerField,
    Func,
    CharField,
    Count,
    ExpressionWrapper, DecimalField,
)
from django.db import transaction
from django.db import connection

# Q is short for query, used to represent a query expression
# for querying expressions, objects.all().filter has no difference with
# objects.filter because of the lazy operation nature


def calculate():
    x = 1
    y = 2
    return x + y


# def say_hello(request):
#     # return HttpResponse('hello, world')
#     # return render(request, 'hello.html')
#     x = 1
#     y = 2
#     z = calculate()
#     return render(request, 'hello.html', {'name': 'Marvin', 'value': z})

def say_hello(request):
    # query_set = Product.objects.all()
    # for product in query_set:
    #     print(product)
    # try:
    #     product = Product.objects.get(pk=0)
    # except ObjectDoesNotExist:
    #     pass
    # for product in query_set:
    #     print(product)

    # product will be None
    # product = Product.objects.filter(pk=0).first()

    # query_set = Product.objects.all().filter(unit_price__lt=20)
    # query_set = Product.objects.all().filter(unit_price__range=(10, 20))
    # query filtering across relationships another_relation__attr (class__attr)
    # inner join
    # query_set = Product.objects.all().filter(collection__id__range=(1, 3))
    # query_set = Product.objects.all().filter(collection__title__icontains='b')

    # query_set = Product.objects.all().filter(name__istartswith='coffee')
    # query_set = Product.objects.all().filter(name__icontains='coffee')

    # year=string or year=number
    # query_set = Product.objects.all().filter(last_updated_at__year=2021)

    # or get(id=1), pk will automatically translates into the primary field

    # query_set = Product.objects.filter(
    #     inventory__lt=10,
    #     unit_price__gt=20
    # )
    # or
    # query_set = Product.objects \
    #     .filter(inventory__lt=10)\
    #     .filter(unit_price__gt=20)

    # Or expression
    # replace parameters with Q objects
    # each Q object takes one parameter and combined with bitwise operators
    # query_set = Product.objects.filter(
    #     Q(inventory__lt=10) | ~Q(unit_price__gt=20)
    # )

    # comparing fields
    # query_set = Product.objects.filter(
    #     inventory=F('unit_price')
    # )
    # query_set = Product.objects.filter(
    #     inventory=F('collection__id')
    # )

    # sorting data
    # query_set = Product.objects.order_by('unit_price', '-name').reverse()

    # get first object
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price')

    # limiting
    # query_set = Product.objects.all()[5:10]

    # reading specific fields
    # instead of getting a list of product instances, we get a list of dicts
    # query_set = Product.objects.values('id', 'name', 'collection__title')
    # we get a list of tuples
    # query_set = Product.objects.values_list('id', 'name', 'collection__title')

    # find the products that have been ordered and sort the results
    # query_set = Product.objects.filter(
    #     id__in=OrderItem.objects.values('product__id').distinct()
    # ).order_by('name')

    # SQL queries are exactly the same as the previous one
    # pass queries will not result to evaluation of the query
    # query_ids = OrderItem.objects.values('product__id').distinct()
    # query_set = Product.objects.filter(
    #     id__in=query_ids
    # ).order_by('name')

    # the difference between only() and values() is that only() returns a list
    # of objects, but the objects only have the fields specified in the parameters
    # the missing parameter can be accessed by automatically issuing an extra query
    # query_set = Product.objects.all().only('name', 'unit_price')[:5]
    # query_set = Product.objects.all().defer('description')[:5]

    # select related on foreign key will join the related tables at the database
    # and select the related records
    # we use select_related when the other end of the relationship has only one instance

    # query_set = Product.objects.select_related('collection__featured_product').all()[:5]

    # prefetch_related will select the related records on the current table
    # and then find the related records on the other tables
    # no joining between two ends of the relationship at the database
    # the joining happens in memory
    # we use prefetch_related when the other end of the relationship has many instances

    # query_set = Product.objects.prefetch_related('promotions').all()[:5]
    # query_set = Product.objects \
    #     .prefetch_related('promotions') \
    #     .select_related('collection') \
    #     .all()[:5]

    # get the last 5 orders with their customers and items (including the products)

    # the reason we can use orderitem_set here:
    # orderitem_set is the manager to get all related objects from one order instance
    # query_set = Order.objects\
    #     .prefetch_related('orderitem_set__product')\
    #     .select_related('customer')\
    #     .order_by('-placed_at')[:5]

    # test related_name and related_query_name
    # https://stackoverflow.com/questions/60119027/what-is-related-name-and-related-query-name-in-django/60120968
    # https://stackoverflow.com/questions/43132872/difference-between-related-name-and-related-query-name-attributes-in-django/43133136
    # https://stackoverflow.com/questions/4601703/difference-between-one-to-many-and-many-to-one-relationship
    # related_query_name is used to filter the current table
    # by joining the other table and specifying the attributes in the other table
    # related_name is a manager which is used to get the related objects from one
    # instance of the foreign key

    # customers = Customer.objects.filter(order__id__lt=20)
    # list(customers)
    # orders = customers[0].order_set.all()
    # list(orders)

    # related_query_name is default to model name with small cases
    # if related_name is manually set, the related_query_name is default to
    # the changed related_name

    # customers = Customer.objects.filter(orders__id__lt=20)
    # list(customers)
    # orders = customers[0].orders.all()
    # list(orders)

    # the result is a dict
    # result = Product.objects.aggregate(
    #     count=aggregates.Count('id'),
    #     min_price=aggregates.Min('unit_price'),
    # )

    # aggregate is working on querySet
    # result = Product.objects.filter(id__lt=20).aggregate(
    #     count=aggregates.Count('id'),
    #     min_price=aggregates.Min('unit_price'),
    # )

    # add additional attributes to the objects while querying them

    # we need to pass Expression object to annotate().
    # base class for all expression: Expression
    # -> subclasses:
    #  Value: wrap values
    #  F: refer to fields,
    #  Func: call database functions
    #  Aggregate: base class for all aggregation functions
    #  ExpressionWrapper: building complex expressions

    # query_set = Customer.objects.annotate(is_new=Value(True, output_field=IntegerField()))
    # query_set = Customer.objects.annotate(new_id=F('id')+1)

    # call database functions
    # query_set = Customer.objects.annotate(
    #     full_name=Func(
    #         F('first_name'),
    #         Value(' ', output_field=CharField()),
    #         F('last_name'),
    #         function="CONCAT",
    #     )
    # )

    # query_set = Customer.objects.annotate(
    #     full_name=Concat(
    #         'first_name',
    #         Value(' ', output_field=CharField()),
    #         'last_name',
    #     )
    # )

    # query_set = Customer.objects.annotate(
    #     # should be order_set, but somehow this function implements with just order
    #     orders_count=Count('order')
    # )

    # query_set = Product.objects.annotate(
    #     discount_price=ExpressionWrapper(
    #         F('unit_price') * 0.8,
    #         output_field=DecimalField(),
    #     )
    # )

    # get for model is a special method, only available for ContentType manager
    # can't just use the id in the database, because the id might be different
    # for databases
    # content_type = ContentType.objects.get_for_model(Product)
    # query_set = TaggedItem.objects.filter(
    #     content_type=content_type,
    # ).select_related('tag')

    # query_set = TaggedItem.objects.get_for_object(Product, 1)

    # query_set = Product.objects.all()
    # list(query_set) will evaluate the query
    # and store the results from database in memory the query set cache
    # the second time, list(query_set) is called,
    # it will read the results from memory

    # one query
    # result = list(query_set)
    # product = query_set[0]

    # two queries,
    # caching happens only if you evaluate the entire query first
    # product = query_set[0]
    # result = list(query_set)

    # create new record

    # collection = Collection()
    # collection.title = 'video games'
    # collection.featured_product = Product(pk=1)
    # # collection.featured_product_id = 1
    # collection.save()
    #
    # collection = Collection(
    #     title='video games2',
    #     featured_product=Product(pk=2)
    # )
    # collection.save()
    # collection = Collection.objects.create(
    #     title='video games3',
    #     featured_product=Product(pk=3)
    # )

    # updating records

    # the missing attributes will be set to default none value of its type by python
    # collection = Collection(pk=11)
    # collection.title = 'games'
    # collection.featured_product = Product(pk=5)
    # collection.save()
    #
    # collection = Collection.objects.get(pk=11)
    # print(collection.featured_product.id)
    # collection.featured_product = Product(pk=11)
    # collection.save()

    # cannot use get, update only works on queryset
    # Collection.objects.filter(pk=11).update(featured_product=Product(pk=14))

    # deleting records

    # delete single record
    # collection = Collection(pk=12)
    # collection.delete()
    #
    # # delete multiple records
    # Collection.objects.filter(id__gt=10).delete()

    # transaction

    return render(
        request,
        'hello.html',
        {
            'name': 'Marvin',
            # 'customers': list(query_set),
            # 'orders': list(query_set)
            # 'result': result,
            # 'tags': list(query_set),
        }
    )


# transaction

# a decorator
# @transaction.atomic()
def say_hello2(request):
    # context manager
    # ...
    # with transaction.atomic():
    #     order = Order()
    #     order.customer = Customer(1)
    #     order.save()
    #
    #     item = OrderItem()
    #     item.order = order
    #     item.product = Product(-1)
    #     item.unit_price = 10
    #     item.quantity = 10
    #     item.save()

    # query_set = Product.objects.raw(
    #     'SELECT * FROM store_product'
    # )

    # don't map the records to Model objects,
    # we can access the database directly and bypass the model layer

    with connection.cursor() as cursor:
        # with to replace try and finally
        cursor.execute(
            'SELECT * FROM store_product'
        )
        # call stored procedures in database
        # with name and parameters
        # cursor.callproc('get_customers', ['1', 2, 'a'])

    return render(
        request,
        'hello.html',
        {
            'name': 'Marvin',
            # 'customers': list(query_set),
            # 'orders': list(query_set)
            # 'result': result,
            # 'tags': list(query_set),
            # 'query_set': list(query_set)
        }
    )
