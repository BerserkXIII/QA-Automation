

import requests
import pytest
import allure
import constants

def test_get_products_list():
    response = requests.get(f"{constants.API_BASE_URL}/productsList")
    data = response.json()
    assert data["responseCode"] == 200
    assert response.status_code == 200
    for _ in response.json()["products"]:
        assert "id" in _
        assert "name" in _
        assert "price" in _
        assert "brand" in _
        assert "category" in _
    
def test_post_products_list():
    payload = {
        "name": "Test Product",
        "price": "100",
        "brand": "Test Brand",
        "category": "Test Category"
    }
    response = requests.post(f"{constants.API_BASE_URL}/productsList", data=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["responseCode"] == 405

def test_post_create_account():
    payload = {"name": "Test User", "email":f"{constants.crear_usuario_nuevo()['email']}", "password": "password", 
               "title": "Mr", "birth_date": "1", "birth_month": "1", "birth_year": "1990", 
               "firstname": "Test", "lastname": "User", "company": "Test Company", "address1": "123 Test St", "address2": "",
                "country": "United States", "zipcode": "12345", "state": "CA", "city": "Test City", "mobile_number": "1234567890"}
    response = requests.post(f"{constants.API_BASE_URL}/createAccount", data=payload)
    assert response.status_code == 200
    assert response.json()["responseCode"] == 201
    assert response.json()["message"] == "User created!"
    check = requests.get(f"{constants.API_BASE_URL}/getUserDetailByEmail", params={"email": payload["email"]})
    user_data = check.json()["user"]
    mapeo = {"birth_date": "birth_day", "firstname": "first_name", "lastname": "last_name", }
    campos_a_comparar = ["name", "title", "birth_date", "birth_month", "birth_year", "email",
                         "firstname", "lastname", "company", "address1", "address2", "country", "zipcode", "state", "city"]
    for campo in campos_a_comparar:
        campo_en_respuesta = mapeo.get(campo, campo)
        assert str(user_data[campo_en_respuesta]) == str(payload[campo])

def test_delete_created_user(usuario_temporal):
    usuario = usuario_temporal
    response = requests.delete(f"{constants.API_BASE_URL}/deleteAccount", data={"email": usuario["email"], "password": usuario["password"]})
    assert response.status_code == 200
    assert response.json()["responseCode"] == 200
    assert response.json()["message"] == "Account deleted!"