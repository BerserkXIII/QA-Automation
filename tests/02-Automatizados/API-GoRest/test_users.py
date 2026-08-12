

import requests
import pytest
import time
from conftest import BASE_URL


#1
def test_get_users_status_200(headers):
    response = requests.get(f"{BASE_URL}/users", headers=headers, timeout=10)
    assert response.status_code == 200

#2
def test_post_new_user(headers):
    payload = {
        "name": "morpheus",
        "email": f"morpheus{time.time()}@reqres.in",
        "gender": "male",
        "status": "active"
        }
    response = requests.post(f"{BASE_URL}/users", headers=headers, json=payload, timeout=10)
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["gender"] == payload["gender"]
    assert data["status"] == payload["status"]
    user_id = data["id"]
    respones2 = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers)
    assert respones2.status_code == 204

#3
def test_delete_user(headers, usuario_temporal):
    user_id = usuario_temporal["id"]
    response = requests.delete(f"{BASE_URL}/users/{user_id}", headers=headers, timeout=10)
    assert response.status_code == 204

#4
@pytest.mark.parametrize("id_invalido", ["pizza", "999999", "-1", "0"])
def test_get_users_id_invalido(headers, id_invalido):
    response = requests.get(f"{BASE_URL}/users/{id_invalido}", headers=headers, timeout=10  )
    assert response.status_code == 404

#5
def test_patch_user(headers, usuario_temporal):
    payload = {
        "name": "neo",
        "email": f"neo{time.time()}@reqres.in",
        "gender": "female",
        "status": "inactive"
    }
    response = requests.patch(f"{BASE_URL}/users/{usuario_temporal['id']}", headers=headers, json=payload, timeout=10)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["gender"] == payload["gender"]
    assert data["status"] == payload["status"]

#6
def test_rate_limit_headers_presentes(headers):
    response = requests.get(f"{BASE_URL}/users", headers=headers, timeout=10)
    assert response.status_code == 200
    assert "x-ratelimit-limit" in response.headers
    assert "x-ratelimit-remaining" in response.headers
    assert "x-ratelimit-reset" in response.headers
    assert int(response.headers["x-ratelimit-limit"]) > 0

