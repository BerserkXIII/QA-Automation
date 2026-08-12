
import os
import pytest
import requests
import time
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://gorest.co.in/public/v2"

@pytest.fixture
def api_key():
    return os.getenv("GOREST_TOKEN")

@pytest.fixture
def headers(api_key):
    return {"Authorization": f"Bearer {api_key}"}

@pytest.fixture
def usuario_temporal(headers):
    payload = {
        "name": "morpheus",
        "email": f"morpheus{time.time()}@reqres.in",
        "gender": "male",
        "status": "active"
    }
    response = requests.post(f"{BASE_URL}/users", headers=headers, json=payload, timeout=10)
    usuario_creado = response.json()
    yield usuario_creado
    requests.delete(f"{BASE_URL}/users/{usuario_creado['id']}", headers=headers, timeout=10)