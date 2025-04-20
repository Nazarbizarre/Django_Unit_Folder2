from django.urls import path, include

from .views import index, about, product_details, cart_add, cart_detail, cart_delete

app_name = 'products'

urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('product/<int:product_id>/', product_details, name='product_details'),
    path('cart_add/<int:product_id>/', cart_add, name='cart_add'),
    path("cart_detail/", cart_detail, name="cart_detail"),
    path('cart_delete/<int:product_id>/', cart_delete, name="cart_delete"),
    
]