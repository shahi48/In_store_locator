from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('categories/', views.categories, name='categories'),
    path('category/<int:category_id>/', views.category_products, name='category_products'),
    path('add-to-list/<int:product_id>/', views.add_to_list, name='add_to_list'),
    path('remove-from-list/<int:product_id>/', views.remove_from_list, name='remove_from_list'),
    path('product-location/<int:product_id>/', views.get_product_location, name='product_location'),
    path('shopping-list/', views.shopping_list, name='shopping_list'),
    path('update-quantity/<int:item_id>/', views.update_quantity, name='update_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('add-review/<int:product_id>/', views.add_review, name='add_review'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
] 