from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('sales_executive', 'Sales Executive'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='sales_executive')
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    @property
    def is_admin(self):
        return self.role == 'admin'
    
    @property
    def is_manager(self):
        return self.role in ['admin', 'manager']
    
    @property
    def is_sales_executive(self):
        return self.role == 'sales_executive'
        