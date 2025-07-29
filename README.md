Mini ERP System (Backend API)

- **Backend**: Django, Django REST Framework
- **Auth**: Simple JWT
- **Database**: SQLite
- **Others**: django-filter, custom permissions

Features

- JWT-based secure authentication
- Role-based permissions: Admin, Manager, Sales Executive
- Profile update & user account management


Inventory Management
- Full CRUD for products with category support
- Realtime stock tracking
- Customer management system
- Filter, search, and sort functionality
- Inventory overview dashboard

Sales Order System
- Create sales orders with multiple items
- Auto calculate totals and tax (if any)
- Stock validation during order creation
- Order status lifecycle:
  `Draft ➡ Confirmed ➡ Shipped ➡ Delivered ➡ Cancelled`

Role-Based Permissions

 Role                    Capabilities                                             
    Sales Executive -   Create/View **only their** orders                        
    Manager          -  Manage inventory, view all orders                        
    Admin            -  Full system access, including user and role management   


Advanced Features
- Unique auto-incremented order numbers
- Atomic transactions for orders (stock deducted only on confirm)
- RESTful API with consistent status codes and error handling
- Scalable app structure for future extensions

User Roles

- **Admin**: Full access
- **Manager**: Inventory + order read access
- **Sales Executive**: Can create/view own orders only

Project Structure


    mini_erp/
    ├── apps/
    │ ├── users/
    │ ├── inventory/
    │ └── sales/
    ├── mini_erp/
    │ └── settings.py
    ├── manage.py
    ├── requirements.txt
    └── .env

Clone the Repository
<pre> python git clone https://github.com/yourusername/yourrepo.git
    cd yourrepo 
</pre>


Setup

1. Create Virtual Env

    <pre> 
    python -m venv venv
    source venv/bin/activate #linux
    venv\Scripts\activate #windows
    </pre>

         

2. Install Dependencies

    <pre> 
    pip install -r requirements.txt
    </pre>

        


3. Setup Environment Variables

    <pre> 
    SECRET_KEY=your-secret-key
    DEBUG=True
    </pre>

        

4. Initialize Database

    <pre> 
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    </pre>

        

5. Run the Server
    <pre> 
    python manage.py runserver
    </pre>


Access
    <pre> 
        http://127.0.0.1:8000/admin/     #Admin
        http://127.0.0.1:8000/api/   #API root
    </pre>



    

    


API Documentation and Usage Examples

### Authentication Endpoints
```
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/logout/
POST /api/auth/token/refresh/
GET  /api/auth/profile/
GET  /api/auth/users/         (Admin only)
```

### Inventory Endpoints
```
GET    /api/inventory/dashboard/
GET    /api/inventory/categories/
POST   /api/inventory/categories/
GET    /api/inventory/categories/{id}/
PUT    /api/inventory/categories/{id}/
DELETE /api/inventory/categories/{id}/

GET    /api/inventory/products/
POST   /api/inventory/products/
GET    /api/inventory/products/{id}/
PUT    /api/inventory/products/{id}/
DELETE /api/inventory/products/{id}/

GET    /api/inventory/customers/
POST   /api/inventory/customers/
GET    /api/inventory/customers/{id}/
PUT    /api/inventory/customers/{id}/
DELETE /api/inventory/customers/{id}/
```

### Sales Endpoints
```
GET  /api/sales/dashboard/
GET  /api/sales/orders/
POST /api/sales/orders/
GET  /api/sales/orders/{id}/
PUT  /api/sales/orders/{id}/
DELETE /api/sales/orders/{id}/
POST /api/sales/orders/{id}/confirm/


# Register a New User

# POST /api/auth/register/

{
    "username": "user",
    "email": "email@gmail.com",
    "role": "user",
    "password": "user",
    "password_confirm": "user"
  }

# POST /api/auth/login/
{
    "username": "username",
    "password": "password"
}

# Response:
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "username",
        "email": "email@gmail.com",
        "first_name": "first_name",
        "last_name": "last_name",
        "role": "sales_executive"
    }
}

# Create a Product
POST /api/inventory/products/
{
    "name": "Product1",
    "sku": "TP-001",
    "category": 1,
    "quantity": 100,
    "unit_price": "499.99"
    "description": "High-performance laptop for business use"
  }

# Create Customer

POST /api/inventory/customers/
{
    "name": "ABC Technologies",
    "email": "contact@abctech.com",
    "phone": "9876543210",
    "address": "123 Tech Park, Mumbai",
    "gstin": "27AABCU9603R1ZM"
}

# Create Sales Order
# POST /api/sales/orders/
{
    "customer": 1,
    "notes": "Urgent delivery required",
    "items": [
        {
            "product": 1,
            "quantity": 2,
            "unit_price": "75000.00"
        },
        {
            "product": 2,
            "quantity": 1,
            "unit_price": "25000.00"
        }
    ]
}

# Confirm Sales Order

# POST /api/sales/orders/1/confirm/
# This will automatically reduce inventory quantities
