from django.urls import path
from . import views

urlpatterns = [
     path('',views.marketplace, name = "marketplace"),
      # Card page
     path('cart/',views.cart,name='cart'),
     # Path for the vendor details(vendor name,food categories,food items).
     path('<slug:vendor_slug>/',views.vendor_detail,name='vendor_detail'),
     # Adding the food items to cart.
     path('add_to_cart/<int:food_id>/',views.add_to_cart,name='add_to_cart'),
     # Decrease the fodd items to cart.
     path('decrease_cart/<int:food_id>/',views.decrease_cart,name='decrease_cart'),
     # Delete cart item.
     path('delete_cart/<int:cart_id>/',views.delete_cart,name='delete_cart'),

]
