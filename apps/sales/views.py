from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count
from .models import SalesOrder, SalesOrderItem
from .serializers import SalesOrderSerializer, SalesOrderListSerializer
from apps.users.permissions import IsSalesExecutiveOrManager

@api_view(['GET'])
def sales_dashboard(request):
    if request.user.is_manager:
        orders = SalesOrder.objects.all()
    else:
        orders = SalesOrder.objects.filter(created_by=request.user)
    
    total_orders = orders.count()
    confirmed_orders = orders.filter(status='confirmed').count()
    draft_orders = orders.filter(status='draft').count()
    total_revenue = orders.filter(status__in=['confirmed', 'shipped', 'delivered']).aggregate(
        total=Sum('total_amount')
    )['total'] or 0
    
    return Response({
        'total_orders': total_orders,
        'confirmed_orders': confirmed_orders,
        'draft_orders': draft_orders,
        'total_revenue': float(total_revenue),
    })

class SalesOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = SalesOrderSerializer
    permission_classes = [IsSalesExecutiveOrManager]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'customer']
    search_fields = ['order_number', 'customer__name']
    ordering_fields = ['created_at', 'total_amount']
    
    def get_queryset(self):
        if self.request.user.is_manager:
            return SalesOrder.objects.all()
        else:
            return SalesOrder.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return SalesOrderListSerializer
        return SalesOrderSerializer

class SalesOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SalesOrderSerializer
    permission_classes = [IsSalesExecutiveOrManager]
    
    def get_queryset(self):
        if self.request.user.is_manager:
            return SalesOrder.objects.all()
        else:
            return SalesOrder.objects.filter(created_by=self.request.user)

@api_view(['POST'])
def confirm_order(request, pk):
    """Confirm a sales order and reduce inventory"""
    try:
        if request.user.is_manager:
            order = SalesOrder.objects.get(pk=pk)
        else:
            order = SalesOrder.objects.get(pk=pk, created_by=request.user)
        
        if order.status != 'draft':
            return Response(
                {'error': 'Only draft orders can be confirmed'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.confirm_order()
        serializer = SalesOrderSerializer(order)
        return Response({
            'message': 'Order confirmed successfully',
            'order': serializer.data
        })
        
    except SalesOrder.DoesNotExist:
        return Response(
            {'error': 'Order not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

