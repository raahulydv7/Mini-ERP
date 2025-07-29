from django.shortcuts import render

# Create your views here.
from rest_framework import generics, filters, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product, Customer
from .serializers import CategorySerializer, ProductSerializer, CustomerSerializer
from apps.users.permissions import IsAdminOrManager

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrManager]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrManager]

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrManager]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active']
    search_fields = ['name', 'sku', 'description']
    ordering_fields = ['name', 'created_at', 'unit_price', 'quantity']

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrManager]

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.filter(is_active=True)
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrManager]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'email', 'phone', 'gstin']
    ordering_fields = ['name', 'created_at']

class CustomerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminOrManager]

@api_view(['GET'])
def inventory_dashboard(request):
    """Dashboard endpoint for inventory statistics"""
    if not request.user.is_manager:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
    total_products = Product.objects.filter(is_active=True).count()
    out_of_stock = Product.objects.filter(is_active=True, quantity=0).count()
    low_stock = Product.objects.filter(is_active=True, quantity__lte=10, quantity__gt=0).count()
    total_customers = Customer.objects.filter(is_active=True).count()
    
    return Response({
        'total_products': total_products,
        'out_of_stock': out_of_stock,
        'low_stock': low_stock,
        'total_customers': total_customers,
    })