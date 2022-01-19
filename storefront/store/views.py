import http

from django.db.models.aggregates import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, DjangoModelPermissions, \
    DjangoModelPermissionsOrAnonReadOnly
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from core.serializers import UserSerializer
from store.filters import ProductFilter
from store.models import Product, Collection, OrderItem, Review, Cart, CartItem, Customer, Order
from store.paginations import ProductPageNumberPagination
from store.permissions import IsAdminOrReadOnly, FullDjangoModelPermissions, ViewCustomerHistoryPermission
from store.serializers import (
    ProductSerializer,
    CollectionSerializer,
    ProductSerializerForCreate,
    ReviewSerializer, CartSerializer, CartItemSerializer, CartItemSerializerForCreate, CartItemSerializerForUpdate,
    CustomerSerializer, OrderSerializer, OrderSerializerForCreate, OrderSerializerForUpdate
)

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, \
    UpdateModelMixin
from django_filters.rest_framework import DjangoFilterBackend


# this backend gives generic filtering
# gt or lt need the custom filter class


# get the browsable API,
# which makes it easy to test the API endpoints in the browser
# the heading is generated based on the view function
# the information of the request we received
# the information about the response
#   the status of the response
#   Allow: what http methods are supported at this endpoint
#   Vary: for caching
#   the body of the response


# @api_view()
# def product_detail(request: Request, obj_id: str) -> Response:
#     # print(type(obj_id))
#     return Response({obj_id, 'ok'})

# def product_list(request: HttpResponse) -> HttpResponse:
#     return HttpResponse('ok')

# @api_view()
# def product_detail(request: Request, obj_id: int) -> Response:
#
#     # first argument is the Model, second is the lookup parameter
#     product = get_object_or_404(Product, pk=obj_id)
#     # product = Product.objects.get(pk=obj_id)
#     # when this serializer is created,
#     # it converts the object passed in to a dict
#     serializer = ProductSerializer(product)
#     # get the dict from serializer by .data
#     product_data = serializer.data
#     # JSONRenderer will convert this dict into JSON object under the hood
#     return Response(product_data)


#     try:
#         product = Product.objects.get(pk=obj_id)
#         serializer = ProductSerializer(product)
#         product_data = serializer.data
#         return Response(product_data)
#     except Product.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if an object doesn't exist, we should not raise an exception
#     but return 404

# @api_view()
# def product_list(request: Request) -> Response:
#     # to avoid lazy loading in serializers
#     products = Product.objects.select_related('collection').all()
#     # products = Product.objects.all()
#     # serializer = ProductSerializer(products, many=True)
#     # provide with request for hyperlinked relation
#     serializer = ProductSerializer(
#         products, many=True, context={'request': request}
#     )
#     return Response(serializer.data)


# final version before introducing class based views


# @api_view(['GET', 'PUT', 'DELETE'])
# def product_detail(request: Request, obj_id: int) -> Response:
#     product = get_object_or_404(Product, pk=obj_id)
#     if request.method == 'GET':
#         serializer = ProductSerializer(
#             product, context={'request': request}
#         )
#         product_data = serializer.data
#         return Response(product_data)
#     elif request.method == 'PUT':
#         # if we pass an instance in the serializer, (instantiating a serializer)
#         # it'll try to update the attributes of that instance
#         # using the data passed in
#         serializer = ProductSerializerForCreate(
#             instance=product, data=request.data
#         )
#         # print(f"raw data 0: {serializer.initial_data}")
#         serializer.is_valid(raise_exception=True)
#         # print(f"raw data 1: {serializer.validated_data}")
#         serializer.save()
#         # serializer.data is updated after calling .save()
#         # serializer.data can only be inspected after calling save()
#         # print(f"updated data: {serializer.data}")
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         if product.orderitem_set.count() > 0:
#             return Response(
#                 {"error": "Product can't be deleted, "
#                           "it's associated with some orders"},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         product.delete()
#         return Response(
#             {"Deleted": "success"},
#             status=status.HTTP_204_NO_CONTENT
#         )


# @api_view(['GET', 'POST'])
# def product_list(request: Request) -> Response:
#     print('request', request)
#     if request.method == 'GET':
#         products = Product.objects.select_related('collection').all()[:10]
#         serializer = ProductSerializer(
#             products, many=True, context={'request': request}
#         )
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ProductSerializerForCreate(data=request.data)
#         # the same as the if else statement
#         # DRF will automatically return a response with 400
#         # and serializer.errors
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         print('validated_data', serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
#         # if serializer.is_valid():
#         #     serializer.validated_data
#         #     return Response('ok')
#         # else:
#         #     return Response(
#         #         serializer.errors,
#         #         status=status.HTTP_400_BAD_REQUEST
#         #     )

# @api_view(['GET', 'PUT', 'DELETE'])
# def collection_detail(request: Request, obj_id) -> Response:
#     collection = get_object_or_404(
#         Collection.objects.annotate(
#             product_count=Count('product')
#         ),
#         pk=obj_id)
#     if request.method == 'GET':
#         serializer = CollectionSerializer(collection)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CollectionSerializer(
#             instance=collection, data=request.data
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         product_count = collection.product_set.count()
#         if product_count > 0:
#             return Response(
#                 data={"error":
#                 "The collection can't be deleted,
#                 it has products in this collection"
#                 },
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         collection.delete()
#         return Response(status=status.HTTP_200_OK)


# @api_view(['GET', 'POST'])
# def collection_list(request: Request) -> Response:
#
#     # print(repr(CollectionSerializer()))
#
#     if request.method == 'GET':
#         query_set = Collection.objects.annotate(
#             product_count=Count('product')
#         ).all()
#         serializer = CollectionSerializer(query_set, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#     elif request.method == 'POST':
#         serializer = CollectionSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


#  APIView class is base class for all class based classes
# class-based views

# class ProductList(APIView):
#
#     def get(self, request: Request):
#         products = Product.objects.select_related('collection').all()[:10]
#         serializer = ProductSerializer(
#             products, many=True, context={'request': request}
#         )
#         return Response(serializer.data)
#
#     def post(self, request: Request):
#         serializer = ProductSerializerForCreate(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         print('validated_data', serializer.validated_data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

# class ProductDetail(APIView):
#     # https://docs.djangoproject.com/en/4.0/topics/class-based-views/intro/
#     # handling-forms-with-class-based-views
#
#     def get(self, request: Request, obj_id: int) -> Response:
#         product = get_object_or_404(Product, pk=obj_id)
#         serializer = ProductSerializer(
#             product, context={'request': request}
#         )
#         product_data = serializer.data
#         return Response(product_data)
#
#     def put(self, request: Request, obj_id: int) -> Response:
#         product = get_object_or_404(Product, pk=obj_id)
#         serializer = ProductSerializerForCreate(
#             instance=product, data=request.data
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def delete(self, request: Request, obj_id: int) -> Response:
#             product = get_object_or_404(Product, pk=obj_id)
#             if product.orderitem_set.count() > 0:
#                 return Response(
#                     {"error": "Product can't be deleted, "
#                               "it's associated with some orders"},
#                     status=status.HTTP_405_METHOD_NOT_ALLOWED,
#                 )
#             product.delete()
#             return Response(
#                 {"Deleted": "success"},
#                 status=status.HTTP_204_NO_CONTENT
#             )


# Mixin is a class that encapsulates some patterns of the codes
# GenericAPIView is the base class for all generic views.
#
# class ProductList(ListCreateAPIView):
#     # the GenericAPIView provides a better creating object api interface
#
#     # queryset and serializer_class in the GenericAPIView can be set directory
#     # without providing the get_methods
#     # to provide the queryset and serializer for the class methods
#     # if there is no logic to set these to values, this way is much simpler
#
#     queryset = Product.objects.select_related('collection').all()
#     # queryset = Product.objects.all()
#     # print(repr(ProductSerializerForCreate()))
#
#     # serializer_class
#
#     # def get_queryset(self):
#     #     return Product.objects.select_related('collection').all()
#
#     def get_serializer_class(self):
#         if self.request.method == 'GET':
#             return ProductSerializer
#         elif self.request.method == 'POST':
#             return ProductSerializerForCreate
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#         # if self.request.method == 'GET':
#         #     return {'request': self.request}
#         # elif self.request.method == 'POST':
#         #     return {}
#
#
# class ProductDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'id'
#     lookup_url_kwarg = 'obj_id'
#
#     def get_serializer_context(self):
#         return {'request': self.request}
#
#     def delete(self, request: Request, *args, **kwargs) -> Response:
#         product = get_object_or_404(Product, pk=kwargs['obj_id'])
#         if product.orderitem_set.count() > 0:
#             return Response(
#                 {"error": "Product can't be deleted, "
#                           "it's associated with some orders"},
#                 status=status.HTTP_405_METHOD_NOT_ALLOWED,
#             )
#         product.delete()
#         return Response(
#             {"Deleted": "success"},
#             status=status.HTTP_204_NO_CONTENT
#         )


# class CollectionList(ListCreateAPIView):
#     queryset = Collection.objects.annotate(
#         product_count=Count('product')
#     ).all()
#     serializer_class = CollectionSerializer
#
#
# class CollectionDetail(RetrieveUpdateDestroyAPIView):
#     queryset = Collection.objects.annotate(
#         product_count=Count('product')
#     ).all()
#     serializer_class = CollectionSerializer
#     # use which field in the model to filter
#     lookup_field = 'id'
#     # receive which parameter and value from request for filtering
#     lookup_url_kwarg = 'obj_id'
#
#     def delete(self, request, *args, **kwargs):
#         collection = get_object_or_404(self.queryset, pk=kwargs['obj_id'])
#         product_count = collection.product_set.count()
#         if product_count > 0:
#             return Response(
#                 data={"error": "The collection can't be deleted, it has products in this collection"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         collection.delete()
#         return Response(status=status.HTTP_200_OK)


# viewset: a set of related views, combine the logic for multiple related
# views inside a single class
# ModelViewSet: combines List, Create, Retrieve, Update, Destroy APIView


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(
        product_count=Count('product')
    ).all()
    serializer_class = CollectionSerializer

    permission_classes = [IsAdminOrReadOnly]

    # lookup_field = 'id'
    # lookup_url_kwarg = 'obj_id'

    def destroy(self, request, *args, **kwargs):
        # collection = get_object_or_404(self.queryset, pk=kwargs['obj_id'])
        # collection = get_object_or_404(self.queryset, pk=kwargs['pk'])
        # product_count = collection.product_set.count()
        if Product.objects.filter(collection=kwargs['pk']).count() > 0:
            return Response(
                data={"error": "The collection can't be deleted, "
                               "it has products in this collection"
                      },
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)


class ProductViewSet(ModelViewSet):
    # Class View defines
    # def setup(self, request, *args, **kwargs):
    #     """Initialize attributes shared by all view methods."""
    #     if hasattr(self, 'get') and not hasattr(self, 'head'):
    #         self.head = self.get
    #     self.request = request
    #     self.args = args
    #     self.kwargs = kwargs

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # with this filter backend, we only need to specify
    # what fields we want to use for filtering in the url+query string

    # filterset_fields = ['collection_id']
    filterset_class = ProductFilter

    # SerachFilter is another filter backend
    search_fields = ['name', 'description']
    # search is case insensitive, and records with the key word
    # inside the corresponding fields will show up

    ordering_fields = ['unit_price', 'last_updated_at']
    # query string ?ordering=-unit_price,last_updated_at
    # sort the results by unit_price descending, and last_updated_at ascending

    # pagination_class = PageNumberPagination
    # the size of each page is set in settings
    # pagination enables to paginate data using page number
    # the return result:
    # instead of a set of products, it returns an object,
    # which has count, next, previous and results

    # pagination_class = LimitOffsetPagination
    # instead of using page number, it uses limit and offset for pagination
    # take limit products and skip offset products, the offset starts from 0

    pagination_class = ProductPageNumberPagination

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.request.method == 'GET':
            queryset = Product.objects.select_related('collection').all()
            # this queryset can support query by query string in the request
            # collection_id = self.request.query_params.get('collection_id')
            # # dict, using get method, if no key, return None
            # if collection_id is not None:
            #     queryset = queryset.filter(collection=collection_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductSerializerForCreate
        return ProductSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    # only admin users can modify products
    # anyone can retrieve a list of products
    # IsAdminUserOrReadOnly
    permission_classes = [IsAdminOrReadOnly]

    # DestroyAPIView has the delete method
    # ModelViewSet doesn't have delete method, it has destroy method
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        # product = get_object_or_404(Product, pk=kwargs['pk'])
        if OrderItem.objects.filter(product=kwargs['pk']).count() > 0:
            return Response(
                {"error": "Product can't be deleted, "
                          "it's associated with some orders"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    # we use context object to provide additional data to the serializer

    # self.kwa
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}

    def get_queryset(self):
        # filter takes product or product_id
        # create can't accept
        return Review.objects.filter(product=self.kwargs['product_pk']).all()

    def list(self, request, *args, **kwargs):
        get_object_or_404(Product, id=self.kwargs['product_pk'])
        # if Product.objects.filter(id=self.kwargs['product_pk']).exists():
        return super().list(request, *args, **kwargs)


class CartViewSet(CreateModelMixin,
                  RetrieveModelMixin,
                  DestroyModelMixin,
                  ListModelMixin,
                  GenericViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        if self.request.method == 'GET':
            return Cart.objects.all().prefetch_related('cartitem_set__product')
        return Cart.objects.all()


class CartItemViewSet(ListModelMixin,
                      RetrieveModelMixin,
                      CreateModelMixin,
                      UpdateModelMixin,
                      DestroyModelMixin,
                      GenericViewSet):
    # not allowing put method for this endpoint
    # the method names here have to be lower cases
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CartItemSerializerForCreate
        elif self.request.method == 'PATCH':
            return CartItemSerializerForUpdate
        return CartItemSerializer

    def get_queryset(self):
        items = CartItem.objects.filter(
            cart=self.kwargs['cart_pk']
        ).all().select_related('product')
        return items

    def get_serializer_context(self):
        if self.request.method == 'POST':
            return {'cart_id': self.kwargs['cart_pk']}
        return {}


# class CustomerViewSet(CreateModelMixin,
#                       RetrieveModelMixin,
#                       UpdateModelMixin,
#                       GenericViewSet):
class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    # permission_classes provide a list of permission classes
    # permission_classes = [IsAuthenticated,]

    # get permissions return a list of objects
    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [IsAuthenticated()]

    # only adminuser can list, create and destroy customers
    permission_classes = [IsAdminUser]

    # user is authenticated and has relevant model permissions
    # to perform operations on that model
    # permission_classes = [FullDjangoModelPermissions]

    # Anonymous users will have read access to data
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    # get customer at customers/me/
    # put to create customer or update customer
    # authenticated users can create or update the associated customers
    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')


class OrderViewSet(ListModelMixin,
                   CreateModelMixin,
                   RetrieveModelMixin,
                   UpdateModelMixin,
                   DestroyModelMixin,
                   GenericViewSet):

    # serializer_class = OrderSerializer

    # only used for create
    # def get_serializer_context(self):
    #     return {'user_id': self.request.user.id}

    # the return result should be the order created not the cart_id
    # overwrite the default create method
    def create(self, request, *args, **kwargs):
        serializer = OrderSerializerForCreate(
            data=request.data,
            context={'user_id': self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        # why the returned data has no items inside
        # problem solved
        # the previous cart successfully created the order and delete the cart
        # the second time pass the cart_id, it creates an order with no items.
        return Response(
            data=OrderSerializer(order).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        instance = self.get_object()
        serializer = OrderSerializer(instance)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            if self.request.method == 'GET':
                return Order.objects.all().prefetch_related('orderitem_set__product')
            return Order.objects.all()

        # violates the command query separation
        # we can embed a logic to create a customer when a user is registered
        # in the save() of UserSerializer
        # (customer_id, created) \
        #     = Customer.objects.only('id').get_or_create(user_id=user.id)

        # implemented in signals to make sure
        # that customer always exists for each user
        customer_id = Customer.objects.only('id').get(user_id=user.id)

        if self.request.method == 'GET':
            return Order.objects.all() \
                .prefetch_related('orderitem_set__product') \
                .filter(customer_id=customer_id)
        return Order.objects.all().filter(customer_id=customer_id)

    # not supports PUT method
    http_method_names = ['get', 'patch', 'post', 'delete', 'head', 'options']

    # permission_classes = [IsAuthenticated]

    def get_permissions(self):
        # if self.request.method in ['PUT', 'PATCH', 'DELETE']:
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderSerializerForCreate
        elif self.request.method == 'PATCH':
            return OrderSerializerForUpdate
        return OrderSerializer

    # def get_serializer_context(self):
    #     serializer = Cart.objects.get(id=self.request.query_params['cart_id'])
    #     return {'cart': serializer}
