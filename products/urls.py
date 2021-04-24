from django.urls import path
from . import views


urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('<int:product_id>/', views.product_detail, name='product_detail'),
]