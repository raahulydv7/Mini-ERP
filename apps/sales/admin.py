from django.contrib import admin
from .models import SalesOrder, SalesOrderItem

class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1
    readonly_fields = ('total_price',)

@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'customer', 'status', 'total_amount', 'created_by', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'customer__name')
    inlines = [SalesOrderItemInline]
    readonly_fields = ('order_number', 'total_amount')

@admin.register(SalesOrderItem)
class SalesOrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'sales_order', 'product', 'quantity', 'unit_price', 'total_price')
    search_fields = ('sales_order__order_number', 'product__name')
    readonly_fields = ('total_price',)
