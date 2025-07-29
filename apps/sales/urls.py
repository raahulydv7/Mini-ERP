from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.sales_dashboard, name='sales-dashboard'),
    path('orders/', views.SalesOrderListCreateView.as_view(), name='sales-order-list'),
    path('orders/<int:pk>/', views.SalesOrderDetailView.as_view(), name='sales-order-detail'),
    path('orders/<int:pk>/confirm/', views.confirm_order, name='confirm-order'),
]