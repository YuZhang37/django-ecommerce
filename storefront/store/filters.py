import django_filters
from django_filters import rest_framework as filters
from store.models import Product


class ProductFilter(filters.FilterSet):
    min_price = django_filters.NumberFilter(
        field_name='unit_price', lookup_expr='gte'
    )
    max_price = django_filters.NumberFilter(
        field_name='unit_price', lookup_expr='lte'
    )

    class Meta:
        model = Product
        # fields = ['collection_id', 'min_price', 'max_price']
        fields = {
            'collection_id': ['exact', ],
            # 'unit_price': ['gt', 'lt'],
        }
