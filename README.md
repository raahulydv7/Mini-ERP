Mini ERP System (Backend API)

- **Backend**: Django, Django REST Framework
- **Auth**: Simple JWT
- **Database**: SQLite (default), easily swappable with PostgreSQL
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
| Role            | Capabilities                                             |
|-----------------|----------------------------------------------------------|
| Sales Executive | Create/View **only their** orders                        |
| Manager         | Manage inventory, view all orders                        |
| Admin           | Full system access, including user and role management   |


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


Setup

1. Create Virtual Env

python -m venv venv
source venv/bin/activate #linux

venv\Scripts\activate #windows 

2. Install Dependencies

pip install -r requirements.txt


3. Setup Environment Variables

SECRET_KEY=your-secret-key
DEBUG=True

4. Initialize Database
bash
Copy code

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

5. Run the Server
python manage.py runserver

Access:

    Admin: http://127.0.0.1:8000/admin/

    API root: http://127.0.0.1:8000/api/


API Endpoints

| Method | Endpoint              | Description       |
| ------ | --------------------- | ----------------- |
| POST   | `/api/auth/register/` | Register new user |
| POST   | `/api/auth/login/`    | JWT login         |
| POST   | `/api/auth/logout/`   | JWT logout        |


Users

| Method | Endpoint         | Description              |
| ------ | ---------------- | ------------------------ |
| GET    | `/api/users/me/` | Get current user profile |
| PATCH  | `/api/users/me/` | Update current profile   |


Inventory
| Method | Endpoint                        | Description       |
| ------ | ------------------------------- | ----------------- |
| GET    | `/api/inventory/products/`      | List all products |
| POST   | `/api/inventory/products/`      | Add new product   |
| PUT    | `/api/inventory/products/<id>/` | Update product    |
| DELETE | `/api/inventory/products/<id>/` | Delete product    |

Customers
| Method | Endpoint                    | Description    |
| ------ | --------------------------- | -------------- |
| GET    | `/api/inventory/customers/` | List customers |
| POST   | `/api/inventory/customers/` | Add customer   |

Sales Orders
| Method | Endpoint                  | Description         |
| ------ | ------------------------- | ------------------- |
| GET    | `/api/sales/orders/`      | List all orders     |
| POST   | `/api/sales/orders/`      | Create new order    |
| PATCH  | `/api/sales/orders/<id>/` | Update order status |
| DELETE | `/api/sales/orders/<id>/` | Cancel/Delete order |


Register a New User

POST  http://127.0.0.1:8000/api/auth/register/

{
    "username": "user",
    "email": "email@gmail.com",
    "role": "user",
    "password": "user",
    "password_confirm": "user"
  }

Create a Product

{
    "name": "Product1",
    "sku": "TP-001",
    "category": 1,
    "quantity": 100,
    "unit_price": "499.99"
  }