from django.urls import path, include

from .views import index, about, product_details

app_name = 'products'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('product/<int:product_id>/', product_details, name='product_details')
]