# 🥭 Mango Selling API

A production-style **Mango Selling REST API** built with **FastAPI**.
The project includes secure authentication, product and category management, Cloudinary image uploads, cash-on-delivery orders, reviews, admin management, email notifications, and Docker-based deployment.

## 🚀 Features

### 🔐 Authentication & User Management

* User registration with email verification
* Account activation through verification link
* JWT-based authentication
* Secure password hashing with Bcrypt
* Login with access token
* Forgot password with email OTP
* OTP expires after 5 minutes
* Password reset using OTP
* Change password for authenticated users
* Profile management
* Role-based access control for Admin and User

### 📂 Category Management

* Category CRUD operations
* Bulk category creation and deletion
* Get all categories
* Get category by ID
* Admin-only management operations

### 🥭 Product Management

* Product CRUD operations
* Bulk product creation and deletion
* Product image upload and deletion using **Cloudinary**
* Product search
* Category-based filtering
* Pagination
* Product reviews

### 🛒 Order Management

* Cash on Delivery (COD)
* Checkout and order creation
* View personal orders
* View order details
* Cancel orders
* Admin can view all orders
* Admin can view individual orders
* Admin can update order status
* Stock is updated when an order is completed

### 📧 Order Email Notifications

* Customer receives an **order confirmation email** after successfully creating an order
* Customer receives an **order completion email** when the admin marks the order as completed

### ⭐ Reviews

* Customers can review purchased products
* Review access is controlled based on order/purchase status

### 👨‍💼 Admin

* Admin authentication and authorization
* Admin dashboard
* Manage categories and products
* View and manage all orders
* Update order status

## 🛠️ Tech Stack

* **Python**
* **FastAPI**
* **SQLAlchemy**
* **PostgreSQL**
* **Alembic**
* **JWT**
* **Bcrypt**
* **SMTP Email**
* **Cloudinary**
* **Docker & Docker Compose**
* **Swagger / OpenAPI**

## 🔄 Authentication Flow

```text
Register
   ↓
Verification Email
   ↓
Activate Account
   ↓
Login
   ↓
JWT Access Token
   ↓
Protected APIs
```

### Password Reset

```text
Forgot Password
   ↓
Enter Email
   ↓
OTP Sent by Email
   ↓
Verify OTP
   ↓
Set New Password
```

## 🛍️ Order Flow

```text
User
 ↓
Browse / Search Products
 ↓
Checkout
 ↓
Cash on Delivery
 ↓
Order Created
 ↓
Order Confirmation Email
 ↓
Admin Updates Status
 ↓
Completed
 ↓
Completion Email
 ↓
Stock Updated
 ↓
Customer Can Review Product
```

## 🖼️ Image Upload

Product images are uploaded to **Cloudinary**.
The application stores the image URL and public identifier in PostgreSQL.

## 📚 API Documentation

After starting the application, Swagger/OpenAPI documentation is available at:

```text
http://localhost:8003/docs
```

Main API modules:

* Users
* Categories
* Products
* Orders
* Admin

## 🐳 Docker Setup

### Start the application

```bash
docker compose up --build
```

### Stop the application

```bash
docker compose down
```

Application:

```text
http://localhost:8003
```

Swagger:

```text
http://localhost:8003/docs
```

## ⚙️ Environment Variables

Create a `.env` file:

```env
DATABASE_URL=your_database_url

SECRET_KEY=your_secret_key

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USERNAME=your_email
EMAIL_PASSWORD=your_app_password

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

> Never commit real credentials or secrets to GitHub.

## 🗂️ Project Structure

```text
Mango_Selling/
│
├── src/
│   ├── users/
│   ├── categories/
│   ├── products/
│   ├── orders/
│   ├── admin/
│   └── utils/
│
├── alembic/
├── seed/
├── Dockerfile
├── docker-compose.yml
├── .env
├── .gitignore
├── requirements.txt
└── main.py
```

## 🔑 Authorization

Protected APIs use JWT authentication and role-based authorization.

```text
JWT Token
    ↓
Current User
    ↓
Role Authorization
    ↓
Protected Resource
```

Resource ownership and business rules are also validated where required.

## 📌 API Overview

| Module     | Operations                                                              |
| ---------- | ----------------------------------------------------------------------- |
| Users      | Register, Activate, Login, Profile, Password Reset, Change Password     |
| Categories | CRUD, Bulk Create/Delete                                                |
| Products   | CRUD, Search, Filtering, Pagination, Images, Reviews                    |
| Orders     | Checkout, Create Order, My Orders, Details, Cancel, Email Notifications |
| Admin      | Dashboard, Product/Category Management, Order Management                |

## 🎯 Project Highlights

* RESTful API architecture with FastAPI
* JWT authentication and role-based authorization
* Email-based account activation and password recovery
* Order confirmation and completion email notifications
* PostgreSQL with SQLAlchemy ORM
* Cloudinary image management
* Cash-on-delivery order workflow
* Stock management after order completion
* Search, filtering, and pagination
* Dockerized application
* Interactive Swagger/OpenAPI documentation

## 👨‍💻 Author

**Jahid Alam**

Python Backend Developer | FastAPI | Django | PostgreSQL | Docker
