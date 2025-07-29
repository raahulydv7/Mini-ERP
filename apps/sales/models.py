from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from apps.inventory.models import Product, Customer
import uuid

User = get_user_model()

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    order_number = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        return f"SO-{uuid.uuid4().hex[:8].upper()}"
    
    def __str__(self):
        return f"{self.order_number} - {self.customer.name}"
    
    def calculate_total(self):
        total = sum(item.total_price for item in self.items.all())
        self.total_amount = total
        self.save()
        return total
    
    def confirm_order(self):
        if self.status != 'draft':
            raise ValidationError("Only draft orders can be confirmed")
        

        for item in self.items.all():
            if item.product.quantity < item.quantity:
                raise ValidationError(f"Insufficient stock for {item.product.name}")
        

        for item in self.items.all():
            item.product.reduce_quantity(item.quantity)
        
        self.status = 'confirmed'
        self.save()

class SalesOrderItem(models.Model):
    sales_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    
    class Meta:
        unique_together = ['sales_order', 'product']
    
    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)

        self.sales_order.calculate_total()
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    def clean(self):
        if self.quantity > self.product.quantity:
            raise ValidationError(f"Insufficient stock. Available: {self.product.quantity}")