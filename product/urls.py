from django.urls import path

from product.views import Posts, ProductCreate

urlpatterns = [
    path('', Posts.as_view()),
    path('create', ProductCreate.as_view())
]