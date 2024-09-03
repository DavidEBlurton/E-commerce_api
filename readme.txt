E-Commerce Flask App

What You Need

Python installed.
MySQL server running.
Postman installed.
Steps to Get Started
1. Install Python Packages
Download the Code: Get the project files.

Set Up Your Environment:

Open a terminal (or command prompt) and go to the project folder.
bash
Copy code
cd path_to_your_project
Create and activate a virtual environment:
bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install required packages:
bash
Copy code
pip install flask flask_sqlalchemy flask_marshmallow mysql-connector-python
1. Set Up the Database
Create a Database:

Open your MySQL client and create a database named ecom:
sql
Copy code
CREATE DATABASE ecom;
Create Tables:

Run the application once to create the tables:
bash
Copy code
python app.py
3. Run the Flask Application
Start the Application:
In the terminal (with virtual environment activated), start the app:
Copy code
python app.py
The app will run at http://127.0.0.1:5000.
4. Test with Postman
Open Postman.

Test Endpoints:

Customers:

Get All Customers: GET http://127.0.0.1:5000/customers
Get Customer by ID: GET http://127.0.0.1:5000/customers/1 (Replace 1 with the ID)
Add Customer: POST http://127.0.0.1:5000/customers
Body (JSON):
json
Copy code
{
  "customer_name": "John Doe",
  "email": "john@example.com",
  "phone": "123-456-7890",
  "username": "johndoe",
  "password": "securepassword"
}
Products:

Get All Products: GET http://127.0.0.1:5000/products
Get Product by ID: GET http://127.0.0.1:5000/products/1 (Replace 1 with the ID)
Add Product: POST http://127.0.0.1:5000/products
Body (JSON):
json
Copy code
{
  "product_name": "Sample Product",
  "price": 19.99,
  "availability": true
}
Orders:

Add Order: POST http://127.0.0.1:5000/orders
Body (JSON):
json
Copy code
{
  "customer_id": 1,
  "items": [1, 2]  // Array of product IDs
}
Get Order by ID: GET http://127.0.0.1:5000/orders/1 (Replace 1 with the ID)
Troubleshooting
Ensure the virtual environment is activated and MySQL server is running.
Check the terminal for error messages if the app doesn’t start.