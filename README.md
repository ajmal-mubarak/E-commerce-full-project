# 🛒 E-Commerce Django Project

A full-featured eCommerce web application built using Django.

---

## 🚀 Features

* User authentication (Login / Register)
* Product listing & categories
* Cart management system
* Wishlist functionality
* Order management
* Razorpay payment integration
* Admin dashboard (customized)

---

## 🛠️ Tech Stack

* Python
* Django
* SQLite (default)
* HTML, CSS, JavaScript
* Razorpay (Payments)

---

## ⚙️ Installation Guide

### 1. Clone the repository

```bash
git clone https://github.com/ajmal-mubarak/E-commerce-full-project.git
cd E-commerce-full-project
```

---

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Mac/Linux:**

```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Apply migrations

```bash
python manage.py migrate
```

---

### 5. Create Admin (Superuser)

```bash
python manage.py createsuperuser
```

Enter:

* Username
* Email
* Password

---

### 6. Run the server

```bash
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000/
```

Admin panel:

```
http://127.0.0.1:8000/admin/
```

Custom Admin panel:

```
http://127.0.0.1:8000/admin_panel/
```

---

## 🔐 Environment Variables

Create a `.env` file in root directory and add:

```
SECRET_KEY=your_secret_key
DEBUG=True

EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

RAZORPAY_KEY_ID=your_key
RAZORPAY_KEY_SECRET=your_secret
```

---

## ⚙️ Additional Setup

### 📧 Email Configuration (Gmail)

1. Go to your Google Account
2. Enable **2-Step Verification**
3. Generate **App Password**
4. Use that password in `.env`

---

### 💳 Razorpay Setup

1. Create account at https://razorpay.com/
2. Go to Dashboard → Settings → API Keys
3. Generate **Test API Keys**
4. Add keys in `.env`

⚠️ Use **Test Mode** during development

---

## 📸 Screenshots

### 🏠 Home Page

![Home](screenshots/home1.jpg)

### 🏠 Home Page (Variant)

![Home](screenshots/home2.jpg)

### 🏠 Home Page (More)

![Home](screenshots/home3.jpg)

### 🛍️ Products Listing

![Products](screenshots/products.jpg)

### 📦 Product Detail

![Product Detail](screenshots/products_detail.jpg)

### 🛒 Cart Page

![Cart](screenshots/cart-page.jpg)

### 🎟️ Coupons Page

![Coupons](screenshots/coupons-page.jpg)

### ❤️ Wishlist

![Wishlist](screenshots/wishlist-page.jpg)

### 🔐 Login Page

![Login](screenshots/login-page.jpg)

### 👤 Profile Page

![Profile](screenshots/profile-page.jpg)

### 📦 My Orders

![Orders](screenshots/myorders-page.jpg)

### ⚙️ Admin Panel (Custom)

![Admin](screenshots/custom-admin.jpg)

### 🔻 Footer Section

![Footer](screenshots/footer.jpg)

---

## 📌 Notes

* Do not commit `.env`, `venv`, or sensitive data
* Use Razorpay test mode for development
* Change email credentials before production

---

## 🔑 Demo Credentials (Optional)

Admin:

```
username: admin
password: admin
```

---

## 👨‍💻 Author

**Ajmal Mubarak**
