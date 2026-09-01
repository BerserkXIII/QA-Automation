
import uuid

HOME_URL = "https://automationexercise.com/"
LOGIN_URL = "https://automationexercise.com/login"
REGISTER_URL = "https://automationexercise.com/signup"
PRODUCTS_URL = "https://automationexercise.com/products"
CART_URL = "https://automationexercise.com/view_cart"
CHECKOUT_URL = "https://automationexercise.com/checkout"
API_BASE_URL = "https://automationexercise.com/api"


def crear_usuario_nuevo():
    email = f"test_{uuid.uuid4().hex[:8]}@test.com"
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": email,
        "password": "Password123",
        "day": "1",
        "month": "January", 
        "year": "1990",
        "address": "123 Test Street",
        "country": "United States",
        "state": "California",
        "city": "New York",
        "zipcode": "10001",
        "phone": "1234567890"
    }

VALID_USER = {
    "title": "Mr",
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@xample.com",
    "password": "pass123",
    "day": "1",
    "month": "January",
    "year": "1990",
    "address": "123 Fake St",
    "country": "United States",
    "state": "California",
    "city": "Los Angeles",
    "zipcode": "90001",
    "mobile_number": "1234567890"
    }

INVALID_USER = {
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "janedoe@xample.com",
    "password": "wrongpassword"}



