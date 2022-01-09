from django.urls import path
from store import views

# url config
urlpatterns = [
    path('products/', views.product_list),
    # apply converter to this parameter,
    # (type converter, otherwise, the type is string)
    # only accepts integer value for the obj_id parameter
    path('products/<int:obj_id>/', views.product_detail),

    # Django rest framework expects a certain convention in the URL,
    # change the parameter name to pk, DRF will read the value of a pk
    # and use it for look up a collection.
    path(
        'collections/<int:obj_id>/',
        views.collection_detail,
        name='collection-detail',
    ),
    path('collections/', views.collection_list),

]