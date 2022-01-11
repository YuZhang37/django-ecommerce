from decimal import Decimal

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from store.models import Product, Collection, Review


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        # id: automatically read-only
        fields = ['id', 'title', 'product_count', 'featured_product']
        read_only_fields = []
        extra_kwargs = {'featured_product': {'required': False}}

    # read_only=True, this field is not for creating and updating
    product_count = serializers.IntegerField(read_only=True)
    # product_count = serializers.IntegerField(required=False)


# {
#     "id": 1002,
#     "name": "abc",
#     "unit_price": 10.0,
#     "collection": 10,
#     "inventory": 100,
#     "others": "hello"
# }

class ProductSerializerForCreate(serializers.ModelSerializer):
    class Meta:
        model = Product
        # when creating or updating, read all the following fields from json,
        # id is not read for creating, autoincrement to get id,
        # id is not read for updating, get from the instance,
        # the fields in object model
        # are initialized with the values of the same fields here,
        # fields here not relevant are discarded, but
        # fields here missing but existing in the object model is set to default None value
        fields = ['id', 'name', 'unit_price', 'collection', 'slug',
                  'inventory',
                  'last_updated_at',
                  # 'title',
                  ]
        # title = serializers.CharField(
        #     max_length=255, source='name',
        # )

    # the default validation rules come from the definition of model fields
    # we need validation at the object level, such as comparing fields.
    # override the validate method in the ModelSerializer

    # def validate(self, validate_data):
    # def validate(self, data):
    #     if data['password'] != data['confirmed_password']:
    #         return ValueError("Passwords don't match")
    #     return data

    # ModelSerializer has a save() method for creating and updating records
    # save() has some logic to extract validated_data and create or update the records

    # we can override how an object is created, like, set some special fields,
    # associate the object with another object in the database.
    # creat() in the ModelSerializer can customize how an object is created
    # takes the validated_data for creation
    # it's called by the save() method when trying to create a new product
    # def create(self, validated_data):
    def create(self, data):
        product = Product(**data)
        product.slug = f'{product.name}-slug'
        product.description = f'this is a product of {product.name}'
        product.save()
        return product

    # DRF will automatically update the matching fields, primary key won't be updated
    def update(self, instance: Product, validated_data):
        super().update(instance, validated_data)
        instance.slug = f'{validated_data["name"]}---slug'
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id',
                  'title',
                  'price',
                  'price_with_tax',
                  'price_with_tax2',
                  'collection', ]

    title = serializers.CharField(max_length=255, source='name')
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price'
    )
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax',
    )
    price_with_tax2 = serializers.DecimalField(
        max_digits=6, decimal_places=2,
        source='get_price_with_tax2',
    )

    collection = serializers.HyperlinkedRelatedField(
        # queryset for inputting/creating records
        queryset=Collection.objects.all(),
        # parameters for generating urls
        # or lookup_field and lookup_url_kwarg default to pk
        view_name='collection-detail',
        # lookup_field='id',
        # lookup_url_kwarg='obj_id',
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class CollectionSerializer0(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer0(serializers.Serializer):
    # we need to decide what fields of the product class we need to serialize
    # what fields we need to include in the python dict.
    # model class: internal representation of the object
    # JSON: external representation of the object.
    # the fields define here will be included in the dict
    # define fields exactly like how to define in the model

    id = serializers.IntegerField()
    # later we will use this serializer to receive data from api
    title = serializers.CharField(max_length=255, source='name')
    # source defaults to the name of the field defines here.
    price = serializers.DecimalField(
        max_digits=6, decimal_places=2, source='unit_price'
    )
    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax',
    )
    price_with_tax2 = serializers.DecimalField(
        max_digits=6, decimal_places=2,
        source='get_price_with_tax2',
    )

    # including related objects in the serializer
    # serializing relationships(foreign key, onetoone, manytomany...)

    # the change detection mechanism doesn't work for providing this queryset
    # represent the foreign key relationship with primary keys of the referred objects
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset=Collection.objects.all(),
    # )

    # represent the foreign key relationship with strings of the referred objects
    # collection = serializers.StringRelatedField()

    # represent the foreign key relationship with the nested referred objects
    # collection = CollectionSerializer()

    # represent the foreign key relationship with the hyperlink of the endpoint
    # for viewing that collection
    collection = serializers.HyperlinkedRelatedField(
        # queryset for inputting/creating records
        queryset=Collection.objects.all(),
        # parameters for generating urls
        view_name='collection-detail',
        # lookup_field='id',
        # lookup_url_kwarg='obj_id',
    )

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'product', 'name', 'description', 'date']
        read_only_fields = ['product', ]
        # extra_kwargs = {'featured_product': {'required': False}}

    def create(self, validated_data):
        product_id = self.context['product_id']
        # return Review.objects.create(product_id=product_id, **validated_data)
        product = get_object_or_404(Product, id=product_id)
        return Review.objects.create(product=product, **validated_data)
