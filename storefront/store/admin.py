from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models import QuerySet
from django.db.models.aggregates import Count
from django.urls import reverse
from django.utils.html import format_html
from django.utils.http import urlencode

from store import models

# tags app has a dependency to the stores app
# so we can't build and deploy independently
# we need to build a new custom app with dependencies on both store and tags app
# and decouple the dependencies between tags and stores apps
# so that both apps are independent reusable apps
# from tags.models import TaggedItem


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'products_count')
    list_per_page = 50

    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # get url from reverse('admin:app_model_page'), don't hardcode it
        # url = reverse('admin:store_product_changelist')

        url_query = urlencode({'collection_id': str(collection.id)})
        url = reverse('admin:store_product_changelist') + '?' + url_query
        html_result = format_html(
            '<a href="{}">{}</a>',  url, collection.products_count,
        )

        # html_result = format_html(
        #     '<a href="http://google.com">{}</a>',
        #     collection.products_count
        # )

        return html_result

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'inventory')
# admin.site.register(models.Product, ProductAdmin)


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'

    def queryset(self, request, queryset: QuerySet):
        # self.value(): the value for the selected filter
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)

    def lookups(self, request, model_admin):
        filters = [
            # (value pass to query parameters, readable notes, show on admin)
            ('<10', 'Low'),
        ]
        return filters


# define the inline form
# tabular inline used for generic objects
# class TagInline(GenericTabularInline):
#     model = TaggedItem
#     autocomplete_fields = ['tag']
#     extra = 0


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # adding collection field will result to a join query in the database to construct
    # the string representation for the collection objects.

    # list_display = ('name', 'unit_price', 'inventory_status', 'collection')

    # list a specific field of collection, can't use __ to refer the field
    list_display = ('name', 'unit_price', 'inventory_status', 'collection_title', 'description')
    list_editable = ('unit_price', )
    list_per_page = 50
    # load related objects in the admin list page
    list_select_related = ('collection', )
    list_filter = ('collection', 'last_updated_at', InventoryFilter)
    actions = ('clear_inventory', )
    search_fields = ('name__istartswith', )

    # fields = ('name', 'slug', 'unit_price')
    # readonly_fields = ('name', )
    exclude = ('promotions', )
    prepopulated_fields = {
        'slug': ('name', ),
    }
    autocomplete_fields = ['collection']

    # inlines = [TagInline, ]

    def collection_title(self, product):
        return product.collection.title

    # specify the fields that shoud be used for sorting the data in this column
    # not supported somehow when changing from django 3.1 to django 3.2
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        # takes an product and calculate some value
        if product.inventory < 10:
            return 'Low'
        return 'OK'

    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset: QuerySet):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            # messages.ERROR,
        )

    # have done for customizing list pages
    # forms for adding or updating models,
    # which is generated based on the definition of the models


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'membership', 'placed_orders')
    ordering = ('first_name', 'last_name')
    list_editable = ('membership',)
    list_per_page = 10
    search_fields = ('first_name__istartswith', 'last_name__istartswith')

    @admin.display(ordering='placed_orders')
    def placed_orders(self, customer):
        url_query = urlencode({'customer_id': str(customer.id)})
        url = reverse('admin:store_order_changelist') + '?' + url_query
        html_result = format_html(
            '<a href="{}">{}</a>',
            url,
            customer.placed_orders,
        )
        return html_result

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            placed_orders=Count('orders')
        )


# TabularInline indirectly inherits from ModelAdmin,
# all attributes of ModelAdmin also applies to ModelAdmin
# class OrderItemInline(admin.StackedInline):
class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    autocomplete_fields = ['product']
    extra = 0
    min_num = 1
    max_num = 3


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'placed_at', 'customer')
    autocomplete_fields = ['customer']

    inlines = [OrderItemInline, ]
