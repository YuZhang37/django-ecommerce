from pprint import pprint

from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter
from rest_framework_nested import routers

from store import views, serializers

# products/2/reviews/1/
# nested resources need nested routers
router = routers.DefaultRouter()

# register parent routers
router.register('collections', views.CollectionViewSet)
router.register('products', views.ProductViewSet, basename='product')
router.register('carts', views.CartViewSet, basename='cart')

# register the child routers
# lookup='product' means /products/product_pk/
# basename is used as the prefix to generate the names of the URL patterns
products_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product'
)
products_router.register(
    'reviews', views.ReviewViewSet,
    basename='product-review'
)

carts_router = routers.NestedDefaultRouter(
    router, 'carts', lookup='cart',
)
carts_router.register(
    'items', views.CartItemViewSet,
    basename='cart-item'
)


# urlpatterns = router.urls + products_router.urls
urlpatterns = [
    path('', include(router.urls)),
    path('', include(products_router.urls)),
    path('', include(carts_router.urls)),
]

# print(repr(serializers.ReviewSerializer()))
# print()
# pprint(router.urls)
# print()
# pprint(products_router.urls)
# print()
# pprint(urlpatterns)
# print(repr(serializers.CartSerializer()))
# print(repr(serializers.CartItemSerializerForCreate()))

# router = DefaultRouter()
# # support Root api
# # support url.json
# # router = SimpleRouter()
# router.register('collections', views.CollectionViewSet)
# router.register('products', views.ProductViewSet, basename='product')
# router.register('reviews')
# # pprint(router.urls)

#
#
# urlpatterns = router.urls




# # url config
# urlpatterns = [
#
#     path('', include(router.urls)),
#     # path('products/', views.product_list),
#
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:obj_id>/', views.ProductDetail.as_view()),
#     # this obj_id parameter will be passed to the view function
#     # the view function will have to have the same parameter with the same name
#     # to receive this argument
#     # when we call as_view(), we will convert this class to a regular class based method
#
#
#     # apply converter to this parameter,
#     # (type converter, otherwise, the type is string)
#     # only accepts integer value for the obj_id parameter
#     # path('products/<int:obj_id>/', views.product_detail),
#
#     # Django rest framework expects a certain convention in the URL,
#     # change the parameter name to pk, DRF will read the value of a pk
#     # and use it for look up a collection.
#     # path(
#     #     'collections/<int:obj_id>/',
#     #     views.collection_detail,
#     #     name='collection-detail',
#     # ),
#
#
#     # path(
#     #     # this request will pass obj_id=value to the handler function
#     #     'collections/<int:obj_id>/',
#     #     views.CollectionDetail.as_view(),
#     #     name='collection-detail',
#     # ),
#     # # path('collections/', views.collection_list),
#     # path('collections/', views.CollectionList.as_view()),
#
# ]