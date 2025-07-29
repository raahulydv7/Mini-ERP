from rest_framework import serializers
from django.db import transaction
from .models import SalesOrder, SalesOrderItem
from apps.inventory.models import Product

class SalesOrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    
    class Meta:
        model = SalesOrderItem
        fields = [
            'id', 'product', 'product_name', 'product_sku',
            'quantity', 'unit_price', 'total_price'
        ]
        read_only_fields = ['total_price']
    
    def validate(self, attrs):
        product = attrs.get('product')
        quantity = attrs.get('quantity')
        
        if quantity <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        
        if quantity > product.quantity:
            raise serializers.ValidationError(
                f"Insufficient stock. Available: {product.quantity}"
            )
        
        return attrs

class SalesOrderSerializer(serializers.ModelSerializer):
    items = SalesOrderItemSerializer(many=True)
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    
    class Meta:
        model = SalesOrder
        fields = [
            'id', 'order_number', 'customer', 'customer_name', 'status',
            'total_amount', 'notes', 'items', 'created_by', 'created_by_name',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['order_number', 'total_amount', 'created_by', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        validated_data['created_by'] = self.context['request'].user
        
        with transaction.atomic():
            sales_order = SalesOrder.objects.create(**validated_data)
            
            for item_data in items_data:
                
                if 'unit_price' not in item_data:
                    item_data['unit_price'] = item_data['product'].unit_price
                
                SalesOrderItem.objects.create(sales_order=sales_order, **item_data)
            
            sales_order.calculate_total()
        
        return sales_order
    
    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        
        if items_data is not None:
            with transaction.atomic():
                
                instance.items.all().delete()
                

                for item_data in items_data:
                    if 'unit_price' not in item_data:
                        item_data['unit_price'] = item_data['product'].unit_price
                    
                    SalesOrderItem.objects.create(sales_order=instance, **item_data)
                
                instance.calculate_total()
        
        return instance

class SalesOrderListSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = SalesOrder
        fields = [
            'id', 'order_number', 'customer_name', 'status', 'total_amount',
            'items_count', 'created_by_name', 'created_at'
        ]
    
    def get_items_count(self, obj):
        return obj.items.count()