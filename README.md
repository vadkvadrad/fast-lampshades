# LampShades MVP E-commerce Application

This is a simple, fast-to-develop e-commerce application built as a temporary solution while a full system is in development. The application follows the requirements from the original request, implementing user registration/login, product browsing, cart functionality, and order management with mock payment.

## 🧰 Tech Stack

| Component | Choice | Reason |
|----------|--------|--------|
| **Language** | Python 3.10+ | Fast development, rich libraries |
| **Framework** | **FastAPI** | Automatic validation, OpenAPI docs, async support |
| **ORM** | **SQLAlchemy** + **Alembic** | Simple mapping, migrations |
| **DB** | **PostgreSQL** | Reliable, JSON support, easy scaling |
| **Auth** | **JWT** (no email confirmation) | Simple, secure, no sessions needed |
| **Deployment** | **Docker + docker-compose** | Single file - and everything works |
| **Proxy** | **nginx** (in docker-compose) | Reverse proxy, TLS in future |

## 🗃️ Database Schema

The application uses 5 tables:

- `users` - user accounts
- `products` - available products
- `carts` - user shopping carts
- `orders` - user orders
- `order_items` - order composition history

## 🧩 API Endpoints

### 🔐 Authentication
- `POST /auth/register` - register user (`email`, `password`)
- `POST /auth/login` - login → returns `access_token` (JWT)

### 🛍️ Products
- `GET /products` - list all products (public)

### 🛒 Cart (requires JWT)
- `POST /cart/items` - add item (`product_id`, `quantity`)
- `DELETE /cart/items/{product_id}` - remove item
- `GET /cart` - get current cart (items + total amount)

### 📦 Orders (requires JWT)
- `POST /orders` - create order (copy cart → `orders` + `order_items`, clear cart)
- `POST /orders/{order_id}/pay` - **mock payment** → status `paid`
- `POST /orders/{order_id}/cancel` - cancel (only if status `pending`)

## 🚀 How to Run

### With Docker (Recommended)
```bash
docker-compose up --build
```

The application will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Manual Setup
1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up the database:
```bash
# Make sure PostgreSQL is running
# Update DATABASE_URL in app/database.py if needed
```

3. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 🏗️ Project Structure

```
lampshades-mvp/
├── app/
│   ├── main.py          # FastAPI entry point
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas (validation)
│   ├── auth.py          # JWT, hashing
│   ├── database.py      # PostgreSQL connection
│   └── api/
│       ├── auth.py      # /auth endpoints
│       ├── products.py  # /products endpoints
│       ├── cart.py      # /cart endpoints
│       └── orders.py    # /orders endpoints
├── alembic/             # migrations
├── Dockerfile
├── docker-compose.yml
├── init.sql             # sample products initialization
└── requirements.txt
```

## ✅ Functionality Covered

| Requirement | Implementation |
|-------------|----------------|
| Registration/login | JWT, bcrypt, `/auth/register`, `/auth/login` |
| View products | `GET /products` (public) |
| Shopping cart | `carts` table, CRUD via API |
| Create order | Copy from `carts` → `orders` + `order_items`, clear cart |
| Cancel order | Only if `status = 'pending'` |
| Mock payment | `POST /orders/{id}/pay` → `status = 'paid'` |

## 💡 Features

- **JWT Authentication** - secure token-based auth
- **Shopping Cart** - add/remove items with quantities
- **Order Management** - create, pay, cancel orders
- **Sample Products** - 8 sample lamp products pre-loaded
- **API Documentation** - automatic Swagger UI at `/docs`

This application is designed for speed and simplicity while fully covering the required functionality. It can be easily extended when needed.
