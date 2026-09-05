
import requests
import time
from conftest import BASE_URL

#1
def test_get_users_status_200(headers):
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    assert response.status_code == 200

#2
def test_get_users_estructura(headers):
    response = requests.get(f"{BASE_URL}/users", headers=headers)
    data = response.json()
    assert "data" in data
    for user in data["data"]:
        assert "id" in user
        assert "email" in user
        assert "first_name" in user
        assert "last_name" in user
        assert "avatar" in user

#3
def test_get_users_paginacion(headers):
    response1 = requests.get(f"{BASE_URL}/users?page=1", headers=headers)
    response2 = requests.get(f"{BASE_URL}/users?page=2", headers=headers)
    data1 = response1.json()
    data2 = response2.json()
    user1 = data1["data"][0]
    user2 = data2["data"][0]
    assert user1["id"] != user2["id"]

#4
def test_get_users_sin_api_key():
    response = requests.get(f"{BASE_URL}/users?_cb={time.time()}")
    print(response.json())
    print(response.status_code)
    #assert response.status_code == 401

#5
def test_get_user_existente(headers):
    user_id = 2
    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    user = data["data"]
    assert user["id"] == user_id

#6
def test_get_user_inexistente(headers):
    user_id = 23
    response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
    assert response.status_code == 404

#7
def test_crear_usuario(headers):
    payload = {
        "name": "morpheus",
        "job": "leader"}
    response = requests.post(f"{BASE_URL}/users", headers=headers, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["job"] == payload["job"]

#8a
def test_crear_usuario_sin_datos(headers):
    payload = {}
    response = requests.post(f"{BASE_URL}/users", headers=headers, json=payload)
    status = response.status_code
    data = response.json()
    assert "name" not in data
    assert status == 201

#8b
def test_crear_usuario_datos_aleatorios(headers):
    payload = {"partidas": 10, "puntos": 100}
    response = requests.post(f"{BASE_URL}/users", headers=headers, json=payload)
    status = response.status_code
    data = response.json()
    assert data["partidas"] == payload["partidas"]
    assert data["puntos"] == payload["puntos"]
    assert status == 201
#9
def test_actualizar_usuario(headers):
    user_id = 2
    payload = {
        "first_name": "morpheus",
        "last_name": "zion"}
    response1 = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
    response2 = requests.put(f"{BASE_URL}/users/{user_id}", headers=headers, json=payload)
    data1 = response1.json()
    data2 = response2.json()
    assert "data" in data1
    assert "data" not in data2
    user1 = data1["data"]
    user2 = data2
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert user1["first_name"] != user2["first_name"]
    assert user1["last_name"] != user2["last_name"]
    assert user2["first_name"] == payload["first_name"]
    assert user2["last_name"] == payload["last_name"]

#10
def test_borrar_usuario(headers):
    user_id = 3
    response1 = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
    response2 = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    assert response1.status_code == 200
    assert response2.status_code == 204