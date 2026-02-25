from django.urls import path
from . import views

urlpatterns = [
    path('', views.item_list, name='home'),
    path('add-to-cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),
    # This is the one we missed!
    path('remove-item/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('adjust/<int:item_id>/<str:action>/', views.adjust_quantity, name='adjust_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
]