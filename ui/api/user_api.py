import requests

from config.config import Config


config = Config()


def get_jwt_token(username, password):
    url = f"{config.BASE_URL}/auth/token"

    form_data = {
        "username": username,
        "password": password
        }

    response = requests.post(url, data=form_data)

    return response.json().get("jwt_token")


def create_user(user_request):
    url = f"{config.BASE_URL}/user/"
    response = requests.post(url, json=user_request)
    return response.json()


def soft_delete(token: str):
    url = f"{config.BASE_URL}/user"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(url, headers=headers)
    return response.json()
