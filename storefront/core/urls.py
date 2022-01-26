from django.urls import path
from django.views.generic import TemplateView


# url config
urlpatterns = [
    path('', TemplateView.as_view(template_name='core/index.html')),
]