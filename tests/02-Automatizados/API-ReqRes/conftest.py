import os
import pytest
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://reqres.in/api"

@pytest.fixture
def api_key():
    return os.getenv("REQRES_API_KEY")

@pytest.fixture
def headers(api_key):
    return {"x-api-key": api_key}