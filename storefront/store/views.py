import http

from django.db.models.aggregates import Count
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from store.models import Product, Collection
from store.serializers import ProductSerializer, CollectionSerializer, ProductSerializerForCreate


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
#     # provide context with request for hyperlinked relation
#     serializer = ProductSerializer(
#         products, many=True, context={'request': request}
#     )
#     return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request: Request, obj_id: int) -> Response:
    product = get_object_or_404(Product, pk=obj_id)
    if request.method == 'GET':
        serializer = ProductSerializer(
            product, context={'request': request}
        )
        product_data = serializer.data
        return Response(product_data)
    elif request.method == 'PUT':
        # if we pass an instance in the serializer, (instantiating a serializer)
        # it'll try to update the attributes of that instance
        # using the data passed in
        serializer = ProductSerializerForCreate(
            instance=product, data=request.data
        )
        # print(f"raw data 0: {serializer.initial_data}")
        serializer.is_valid(raise_exception=True)
        # print(f"raw data 1: {serializer.validated_data}")
        serializer.save()
        # serializer.data is updated after calling .save()
        # serializer.data can only be inspected after calling save()
        # print(f"updated data: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if product.orderitem_set.count() > 0:
            return Response(
                {"error": "Product can't be deleted, "
                          "it's associated with some orders"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        product.delete()
        return Response(
            {"Deleted": "success"},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET', 'POST'])
def product_list(request: Request) -> Response:
    print('request', request)
    if request.method == 'GET':
        products = Product.objects.select_related('collection').all()[:10]
        serializer = ProductSerializer(
            products, many=True, context={'request': request}
        )
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializerForCreate(data=request.data)
        # the same as the if else statement
        # DRF will automatically return a response with 400 and serializer.errors
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print('validated_data', serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


        # if serializer.is_valid():
        #     serializer.validated_data
        #     return Response('ok')
        # else:
        #     return Response(
        #         serializer.errors,
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

@api_view(['GET', 'PUT', 'DELETE'])
def collection_detail(request: Request, obj_id) -> Response:
    collection = get_object_or_404(
        Collection.objects.annotate(
            product_count=Count('product')
        ),
        pk=obj_id)
    if request.method == 'GET':
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CollectionSerializer(
            instance=collection, data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        product_count = collection.product_set.count()
        if product_count > 0:
            return Response(
                data={"error": "The collection can't be deleted, it has products in this collection"},
                status=status.HTTP_400_BAD_REQUEST
            )
        collection.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def collection_list(request: Request) -> Response:

    # print(repr(CollectionSerializer()))

    if request.method == 'GET':
        query_set = Collection.objects.annotate(
            product_count=Count('product')
        ).all()
        serializer = CollectionSerializer(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

