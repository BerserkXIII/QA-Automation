



HOME_URL = "https://parabank.parasoft.com/parabank"
REGISTER_URL = "https://parabank.parasoft.com/parabank/register.htm"
OPEN_ACCOUNT_URL = "https://parabank.parasoft.com/parabank/openaccount.htm"
ACCOUNT_OVERVIEW_URL = "https://parabank.parasoft.com/parabank/overview.htm"
TRANSFER_FUNDS_URL = "https://parabank.parasoft.com/parabank/transfer.htm"
API_BASE_URL = "https://parabank.parasoft.com/parabank/services/bank"

CAMPOS_OBLIGATORIOS = {
    "first_name": {
        "id_error": "customer.firstName.errors",
        "mensaje": "First name is required."    },
    "last_name": {
        "id_error": "customer.lastName.errors",
        "mensaje": "Last name is required."    },
    "address": {
        "id_error": "customer.address.street.errors",
        "mensaje": "Address is required."    },
    "city": {
        "id_error": "customer.address.city.errors",
        "mensaje": "City is required."    },
    "state": {
        "id_error": "customer.address.state.errors",
        "mensaje": "State is required."    },
    "zip_code": {
        "id_error": "customer.address.zipCode.errors",
        "mensaje": "Zip Code is required."    },
    "ssn": {
        "id_error": "customer.ssn.errors",
        "mensaje": "Social Security Number is required."    },
    "username": {
        "id_error": "customer.username.errors",
        "mensaje": "Username is required."    },
    "password": {
        "id_error": "customer.password.errors",
        "mensaje": "Password is required."    },
    "repeated_password": {
        "id_error": "repeatedPassword.errors",
        "mensaje": "Password confirmation is required."
    }
}

PAUSA_ENTRE_TESTS = 5
