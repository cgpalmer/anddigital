from django.urls import path
from . import views


urlpatterns = [
    path('enquiry/', views.customer_enquiry, name='customer_enquiry'),
    path('delivery/', views.delivery_enquiry, name='delivery_enquiry'),
]