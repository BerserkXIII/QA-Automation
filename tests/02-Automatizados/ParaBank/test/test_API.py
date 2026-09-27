

import requests
import json
from constants import API_BASE_URL



def test_get_userID(GET_accountID):
    request = requests.get(f"{API_BASE_URL}/accounts/{GET_accountID[0]['id']}", headers={"Accept": "application/json"})
    assert request.status_code == 200
    assert request.json()["id"] == GET_accountID[0]["id"]


def test_get_accountID(GET_accountID, GET_user_data):
    for cuenta in GET_accountID:
        assert cuenta["customerId"] == GET_user_data["id"]
    accountID_verified = requests.get(f"{API_BASE_URL}/accounts/{GET_accountID[0]['id']}",
                                      headers={"Accept": "application/json"})
    assert accountID_verified.status_code == 200


