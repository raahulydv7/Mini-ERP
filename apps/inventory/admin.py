from django.contrib import admin
from .models import Product, Category, Customer

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'sku', 'category', 'quantity', 'unit_price', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'sku')
    list_editable = ('is_active',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'gstin', 'is_active')
    search_fields = ('name', 'email', 'phone', 'gstin')
    list_filter = ('is_active',)
