from django.urls import path

from playground import views

# url config
urlpatterns = [
    path('hello/', views.say_hello),
    path('hello2/', views.say_hello2),
    path('hello3/', views.say_hello3),
    path('hello4/', views.say_hello4),
    path('hello5/', views.say_hello5),
    path('hello6/', views.say_hello6),
    path('hello7/', views.Hello7View.as_view()),

]