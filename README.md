# Dolphin Threads

Persian RTL Clothing Shop Website built with Django.

## Features

* Custom User Model
* Django Authentication System
* User Profiles
* Product Variants (Color & Size)
* Shopping Cart
* Wishlist
* Order Management
* Product Comments
* AJAX Search
* Welcome Email System
* PostgreSQL Database
* Responsive Design
* Persian RTL UI

## Technologies

* Python
* Django
* PostgreSQL
* Bootstrap 5
* JavaScript
* HTML/CSS

## Screenshots

### Home Page

![Home](screenshots/Home1.png)
![Home](screenshots/Home2.png)

### Product List

![Products](screenshots/Products1.png)
![Products](screenshots/Products2.png)

### Product Detail

![Product Detail](screenshots/Detail1.png)
![Product Detail](screenshots/Detail2.png)

### Shopping Cart

![Cart](screenshots/Cart.png)

### Wishlist

![Wishlist](screenshots/Wishlist.png)

### User Profile

![Profile](screenshots/Profile.png)

### Order History

![Orders](screenshots/Orders.png)

### Admin Panel

![Admin](screenshots/Admin%20Panel.png)

## Project Status

Current Version: v1.0

Future Plans:

- CBV Refactor
- Django REST Framework API
- Payment Gateway Integration
- Deployment

## Installation

Clone repository:

```bash
git clone https://github.com/RealRick37/Dolphin-Threads.git
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` file and configure:

```env
SECRET_KEY=your_secret_key

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your_email
EMAIL_HOST_PASSWORD=your_app_password
```

Run migrations:

```bash
python manage.py migrate
```

Create superuser:

```bash
python manage.py createsuperuser
```

Run development server:

```bash
python manage.py runserver
```

## Language

This project is designed for Persian-speaking users and uses a fully RTL interface.

## More
This project will probably be expanded. 
Hope you guys find it helpful ! :)
